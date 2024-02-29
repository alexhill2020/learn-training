<?php
/**
 * Plugin Name: WP-COS-Integration
 * Plugin URI: http://yourwebsite.com/my-cos-plugin
 * Description: 与腾讯云对象存储服务COS进行交互（A simple plugin to interact with Tencent Cloud COS）。
 * Version: 1.0
 * Author: Yang Changjun
 * Author URI: http://yourwebsite.com
 */



require __DIR__ . '/vendor/autoload.php';

// 插件代码将放置于此处

//初始化COS客户端
use Qcloud\Cos\Client;

$cosClient = new Client([
    'region' => 'ap-chongqing',
    'credentials' => [
        'secretId' => 'AKIDfONQQdv8D5VtEXmwAiP8zvpmmN29LQah',
        'secretKey' => 'ribQCqZICE8AITSH3fL6nYXRF65xjgie',
    ],
]);

//钩子
add_action('admin_post_nopriv_upload_custom_file', 'handle_cos_file_videos_upload');
add_action('admin_post_upload_custom_file', 'handle_cos_file_videos_upload');

//定义上传函数以支持多个标签
//这个函数没有问题，不用修改。
function upload_to_cos_with_tags($bucket, $key, $fileTmpPath, $tags) {
    global $cosClient;
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
        return true;
    } catch (Exception $e) {
        echo "上传或标签设置失败: " . $e->getMessage();
        return false;
    }
}


//下面为批量上传文件的表单
function handle_cos_file_videos_upload() {
    // 显示上传表单和日期选择器
    // 要加选项则直接在这里加，注意，格式一定要和之前的一样。同时，加了选项后一定要记得还要在$tags = []里加标签值。
    // 下面<style></style>里的内容是为表单设计格式。
    if(isset($_FILES['file_to_upload'])) {
        // 文件上传至COS的逻辑
        $bucket = 'ad-1304895350'; // 请替换为实际的存储桶名称
        $keyPrefix = 'videos/'; // 上传文件的前缀路径，可根据需要调整
    
        // 处理每个文件
        foreach ($_FILES['file_to_upload']['name'] as $index => $fileName) {
            $fileTmpPath = $_FILES['file_to_upload']['tmp_name'][$index];
            $key = $keyPrefix . basename($fileName);
    
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
            $uploadSuccess = upload_to_cos_with_tags($bucket, $key, $fileTmpPath, $tags);


            if ($uploadSuccess) {
                echo "文件 '{$fileName}' 上传成功。<br>";
            } else {
                echo "文件 '{$fileName}' 上传失败。<br>";
            }
        }
    }
    
    // 防止WordPress尝试重定向
    //wp_redirect( home_url() );
    //exit;
    
}





