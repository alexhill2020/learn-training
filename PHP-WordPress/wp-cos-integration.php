<?php
/**
 * Plugin Name: Wp-COS-Integration
 * Plugin URI: http://yourwebsite.com/my-cos-plugin
 * Description: 与腾讯云对象存储服务COS进行交互，以将腾讯云COS当作文件存储仓库，并实现文件上传、检索、删除、展示等功能。
 * Version: 1.0
 * Author: Yang Changjun
 * Author URI: http://yourwebsite.com
 */

include_once(plugin_dir_path(__FILE__) . 'cos-settings.php');  //引入并执行cos-settings.php文件，以进行COS客户端相关参数设置。

require __DIR__ . '/vendor/autoload.php';  //加载腾讯云对象存储COS的PHP SDK。


//获取插件设置的函数，以免在后面重复get_option。
function get_wp_cos_integration_settings() {
    // 尝试从缓存中获取设置，避免重复数据库查询
    static $options = null;
    if (null === $options) {
        $options = get_option('wp_cos_integration_settings', []);
    }
    return $options;
}


//初始化COS客户端的函数。
function get_cos_client() {
    
    // 获取插件设置选项
    $options = get_wp_cos_integration_settings();
    
    $required_keys = ['cos_region' => 'region', 'secret_id' => 'SecretID', 'secret_key' => 'SecretKey'];

    foreach ($required_keys as $key => $name) {
        if (empty($options[$key])) {
            wp_die("错误：{$name} 未设置，请先在设置页面中填写 {$name}。");
        }
    }
    
    // // 如果所有必需的设置都已经被正确填写，可以继续执行后续代码。
    $cos_region = $options['cos_region']; 
    $secretId = $options['secret_id']; 
    $secretKey = $options['secret_key']; 
    
    
    $cosClient = new Qcloud\Cos\Client([
        'region' => $cos_region, // 替换为你的COS服务区域
        'credentials' => [
            'secretId'  => $secretId, // 替换为你的腾讯云SecretId
            'secretKey' => $secretKey, // 替换为你的腾讯云SecretKey
        ],
    ]);
    return $cosClient;
}


//此函数主要用正则式法代替basename方法，因为basename方法会让文件名中的中文字符丢失。
function get_basename($fileName){    
     return preg_replace('/^.+[\\\\\\/]/', '', $fileName);    
}


//表单输入检测的script代码。切记只能放到php函数中，不能直接用<script>标签。
function my_custom_inline_script() {
    add_action('wp_enqueue_scripts', function() {
        wp_enqueue_script('jquery');
        $script = <<<EOD
        jQuery(document).ready(function($) {
            // 当任何下拉菜单的选择改变时
            $('select').change(function() {
                // 显示或隐藏“其他”输入框
                showOrHideOtherInput($(this));
            });

            // 表单提交前的验证
            $('#form_to_upload').submit(function(e) {
                var isValid = true;
                var missingSelections = "";

                // 检查文件选择
                if ($('#file_to_upload').get(0).files.length === 0) {
                    alert("未选择任何上传的文件。");
                    e.preventDefault(); // 阻止表单提交
                    return;
                }

                $('select').each(function() {
                    // 检查是否选择了默认选项或“其他”但未填写
                    if ($(this).val() === 'default') {
                        isValid = false;
                        missingSelections += $(this).attr('name') + ", ";
                    } else if ($(this).val() === 'other') {
                        var otherInputId = $(this).attr('id') + '_other';
                        if ($('#' + otherInputId).val().trim() === '') {
                            isValid = false;
                            missingSelections += $(this).attr('name') + " (其他), ";
                        }
                    }
                });

                if (!isValid) {
                    e.preventDefault(); // 阻止表单提交
                    alert("请完成所有标签的选择。未完成选择的标签: " + missingSelections.slice(0, -2));
                }
            });

            function showOrHideOtherInput(select) {
                var selectId = select.attr('id');
                var otherInputId = selectId + '_other';
                if (select.val() === 'other') {
                    $('#' + otherInputId).show();
                } else {
                    $('#' + otherInputId).hide();
                }
            }
        });
EOD;
        wp_add_inline_script('jquery', $script);
    });
}

my_custom_inline_script();


//表单处理逻辑与表单HTML输出函数。
function custom_upload_form_shortcode() {
    
    ob_start();  //启动输出缓冲，因为我们可能会在处理表单提交后输出结果

    // 表单处理逻辑应该放在这里，确保在输出之前处理表单
    if(isset($_FILES['file_to_upload'])) {
        
        
        // 获取插件设置选项
        $options = get_wp_cos_integration_settings();//经测试，先执行这个，而不是上面那个。
        $required_keys = ['cos_region' => 'region', 'cos_bucket' => 'bucket'];
        foreach ($required_keys as $key => $name) {
            if (empty($options[$key])) {
                wp_die("错误：{$name} 未设置，请先在设置页面中填写 {$name}。");
            }
        }
        $bucket = $options['cos_bucket'];
        $region = $options['cos_region']; // 或设定一个默认值

        $keyPrefix = 'videos/'; // 上传文件的前缀路径（也即桶中子文件夹），可根据需要调整。
        
        // 文件上传至COS的逻辑
        // 处理每个文件
        foreach ($_FILES['file_to_upload']['name'] as $index => $fileName) {
            $fileTmpPath = $_FILES['file_to_upload']['tmp_name'][$index];
            //error_log("11111111Uploading file: " . $fileName);  //在日志中第一次输出变量$fileName的值。
            //setlocale(LC_ALL, 'zh_CN.GBK');  //用basename方法的话就用用这一段，主要用于设置区域环境，但可能会影响到程序中其他依赖于区域设置的功能（如字符串格式化、货币格式化等），因此用下面这种方法。
            $fileName = get_basename($fileName); //自定义了一个get_basename函数用于取代basename方法。
            //$key = $keyPrefix . basename($fileName);   //经排查，上传文件中有中文字符，但经过这么一变换之后，就没有中文字符了，确定就是因为这一步引起的，主要是因为basename引起的。添加setlocale(LC_ALL, 'zh_CN.GBK');可解决，但这个可能会影响到程序中其他依赖于区域设置的功能，因此用另一种方法。即正则式法。
            //error_log("222222222Uploading file: " . $fileName);  //在日志中第二次输出变量$fileName的值，以与第一次输出的做对比。
            $key = $keyPrefix . $fileName;
            // 收集标签值。
            // 加了选项后一定要在这里加标签值，否则存储不进去，别忘了。
            $tags = [
                'brand' => $_POST['brand'] === 'other' ? $_POST['brand_other'] : $_POST['brand'],
                'course' => $_POST['course'] === 'other' ? $_POST['course_other'] : $_POST['course'],
                'semester' => $_POST['semester'] === 'other' ? $_POST['semester_other'] : $_POST['semester'],
                'assignment' => $_POST['assignment'] === 'other' ? $_POST['assignment_other'] : $_POST['assignment'],
                'grade' => $_POST['grade'] === 'other' ? $_POST['grade_other'] : $_POST['grade'],
            ];
    
            // 调用之前定义的上传函数，传入文件、标签等参数
            $uploadSuccess = upload_to_cos_with_tags($bucket, $key, $region, $fileTmpPath, $tags);
           
            $fileSize = $uploadSuccess['data']['FileSize'];  //函数upload_to_cos_with_tags返回了data键，这个键包含多个值，这里及下面即是分别取这些值。
            $uploadTime = $uploadSuccess['data']['uploadTime'];
            $fileUrl = $uploadSuccess['data']['FileUrl'];
            $brand = $tags['brand'];
            $course = $tags['course'];
            $semester = $tags['semester'];
            $assignment = $tags['assignment'];
            $grade = $tags['grade'];
    
            if ($uploadSuccess) {
                
                $result = upload_files_info_to_database($fileName, $fileSize, $uploadTime, $fileUrl, $brand, $course, $semester, $assignment, $grade);

                if ($result === true) {
                    echo "文件'<span style='color:green;'> {$fileName} </span>'上传成功，并将信息成功保存到数据库。<br>";
                } else {
                    // $result 存储的是错误信息
                    echo "文'件<span style='color:green;'> {$fileName} </span>'上传成功，但未成功保存信息，错误为：$result";
                }
            } else {
                echo "文'件<span style='color:green;'> {$fileName} </span>'上传失败。<br>";
            }
        }
    }

    // 表单HTML输出，下面的问号和大于号表示后面不是php代码了。
    ?>
    <form action="" method="post" enctype="multipart/form-data" id="form_to_upload">
        <input type="file" name="file_to_upload[]" id="file_to_upload" multiple="multiple"><br>
        创作品牌：<select name="brand" id="brand">
                <option value="default">----请选择----</option>
                <option value="康师傅">康师傅</option>
                <option value="统一">统一</option>
                <option value="白象">白象</option>
                <option value="other">其他...</option>
              </select>
              <input style="display: none;" type="text" name="brand_other" id="brand_other" placeholder="如果其他，请输入"><br>
        课程所属：<select name="course" id="course">
                <option value="default">----请选择----</option>
                <option value="影视广告">影视广告</option>
                <option value="平面广告设计">平面广告设计</option>
                <option value="广告文案">广告文案</option>
                <option value="other">其他...</option>
              </select>
              <input style="display: none;" type="text" name="course_other" id="course_other" placeholder="如果其他，请输入"><br>
        上课学期：<select name="semester" id="semester">
                <option value="default">----请选择----</option>
                <option value="2022-2023-1">2022-2023-1</option>
                <option value="2022-2023-2">2022-2023-2</option>
                <option value="other">其他...</option>
              </select>
              <input style="display: none;" type="text" name="semester_other" id="semester_other" placeholder="如果其他，请输入"><br>
        作业类型：<select name="assignment" id="assignment">
                <option value="default">----请选择----</option>
                <option value="平时作业">平时作业</option>
                <option value="期末作业">期末作业</option>
                <option value="other">其他...</option>
              </select>
              <input style="display: none;" type="text" name="assignment_other" id="assignment_other" placeholder="如果其他，请输入"><br>
        作者年级：<select name="grade" id="grade"> 
                <option value="default">----请选择----</option>
                <option value="本科一年级">本科一年级</option>
                <option value="本科二年级">本科二年级</option>
                <option value="本科三年级">本科三年级</option>
                <option value="本科四年级">本科四年级</option>
                <option value="研究生一年级">研究生一年级</option>
                <option value="研究生二年级">研究生二年级</option>
                <option value="研究生三年级">研究生三年级</option>
                <option value="other">其他...</option>
              </select>
              <input style="display: none;" type="text" name="grade_other" id="grade_other" placeholder="如果其他，请输入"><br>
        <input type="submit" value="上传">
    </form>
    
    <?php   //这里表示下面为php代码。
    // 确保所有的HTML输出都在处理逻辑之后

    return ob_get_clean();  // 返回输出缓冲区的内容
}

add_shortcode('custom_upload_form', 'custom_upload_form_shortcode');  //注册短代码。


//定义上传函数以支持多个标签。
function upload_to_cos_with_tags($bucket, $key, $region, $fileTmpPath, $tags) {

    $cosClient = get_cos_client(); // 获取COS客户端实例
    
    try {
        $cosClient->upload($bucket, $key, fopen($fileTmpPath, 'rb'));
        // 为上传的对象添加多个标签
        $tagSet = [];
        foreach ($tags as $tagKey => $tagValue) {
            if ($tagValue === 'other') {
                $tagValue = isset($tags[$tagKey . '_other']) ? $tags[$tagKey . '_other'] : '';
            }
            if (!empty($tagValue)) { // 确保标签值不为空
                $tagSet[] = ['Key' => $tagKey, 'Value' => $tagValue];
            }
        }
        
        if (!empty($tagSet)) {
            $cosClient->putObjectTagging([
                'Bucket' => $bucket,
                'Key' => $key,
                'TagSet' => $tagSet,
            ]);
        }
        
        $fileUrl = "https://{$bucket}.cos.{$region}.myqcloud.com/{$key}"; // 根据文件的Key拼接文件地址
        $fileSize = filesize($fileTmpPath); // 文件大小
        $uploadTime = date('Y-m-d H:i:s'); // 文件上传时间
                // 以键值对的形式构造返回信息
                
        //error_log("333333333Uploading file: " . $uploadTime);
        $uploadInfo = [
            'FileUrl' => $fileUrl,
            'FileSize' => $fileSize,
            'uploadTime' => $uploadTime,
        ];
        return ['success' => true, 'message' => '文件上传成功', 'data' => $uploadInfo];
    } catch (Exception $e) {
        echo "上传或标签设置失败，请检查后台设置页面<span style='color: blue;'><b>存储桶名称等信息</b></span>是否设置正确。错误信息为:<br> " . $e->getMessage();
        return false;
    }
}


//定义把上传的文件信息写入MySQL数据的函数。
function upload_files_info_to_database($fileName, $fileSize, $uploadTime, $fileUrl, $brand, $course, $semester, $assignment, $grade){
    global $wpdb;
    $table_name = $wpdb->prefix . 'cos_files_informations';
    $data = array(
        'file_name' => $fileName,
        'file_size' => $fileSize,
        'upload_time' => $uploadTime,
        'file_url' => $fileUrl,
        'brand' => $brand,
        'course' => $course,
        'semester' => $semester,
        'assignment' => $assignment,
        'grade' => $grade,
    );
    // 注意：这里假设所有字段都是字符串类型，根据你的实际情况可能需要调整
    $format = array('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
    if($wpdb->insert($table_name, $data, $format)){
        // 数据库操作成功
        return true;
    } else {
        // 数据库操作失败，返回错误信息
        return "数据库操作错误: " . $wpdb->last_error;
    }
}



//--------以下为检索和查询-----------------


function custom_search_form_shortcode() {
    ob_start();
    
     ?>
    <form action="<?php echo esc_url( admin_url('admin-post.php') ); ?>" method="post">
        <input type="hidden" name="action" value="custom_search">
        <label for="file_name">文件名:</label>
        <input type="text" id="file_name" name="file_name"><br>
        <label for="brand">品牌:</label>
        <input type="text" id="brand" name="brand"><br>
        <label for="brand">课程:</label>
        <input type="text" id="course" name="course"><br>
        <!-- 添加更多字段 -->
        <input type="submit" value="检索">
    </form>
    <?php
    return ob_get_clean();
}
add_shortcode('custom_search_form', 'custom_search_form_shortcode');


function custom_search() {
    global $wpdb; // 全局变量，用于数据库操作

    // 确保这个函数只处理POST请求
    if ('POST' !== $_SERVER['REQUEST_METHOD']) {
        return;
    }

    // 检查并清理表单字段
    $file_name = isset($_POST['file_name']) ? sanitize_text_field($_POST['file_name']) : '';
    $brand = isset($_POST['brand']) ? sanitize_text_field($_POST['brand']) : '';
    $course = isset($_POST['course']) ? sanitize_text_field($_POST['course']) : '';
    // 添加其他字段...

    // 构建基础查询语句
    $query = "SELECT * FROM wp_cos_files_informations WHERE 1=1"; // 注意“wp_cos_files_informations”为表名，一定要跟数据库的表名一模一样。

    // 根据用户输入添加条件
    if (!empty($file_name)) {
        $query .= $wpdb->prepare(" AND file_name LIKE %s", '%'.$file_name.'%');
    }
    if (!empty($brand)) {
        $query .= $wpdb->prepare(" AND brand = %s", $brand);
    }
    if (!empty($course)) {
        $query .= $wpdb->prepare(" AND course = %s", $course);
    }
    // 添加其他字段的条件...

    // 执行查询
    $results = $wpdb->get_results($query);
    
    //error_log('44444444444Executed query: ' . $wpdb->last_query);

    // 检查并显示结果
    if (!empty($results)) {
        foreach ($results as $row) {
            echo '<div>';
            echo '<p>File Name: ' . esc_html($row->file_name) . '</p>';
            echo '<p>File Url: ' . esc_html($row->file_url) . '</p>';
            // 输出其他字段...
            echo '</div>';
        }
    } else {
        echo '<p>No results found.</p>';
    }

    die(); // 防止WordPress进一步处理或重定向
}
add_action('admin_post_nopriv_custom_search', 'custom_search');  //此为钩子，钩子中的函数名一定要正确。
add_action('admin_post_custom_search', 'custom_search');

