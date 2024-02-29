<?php
/* Template Name: Custom Upload Page */

get_header(); // 获取网站头部

// 页面内容开始
?>

<div class="container">
    <h1>Upload Your File</h1>
    <form action="<?php echo admin_url('admin-post.php'); ?>" method="post" enctype="multipart/form-data" id="form_to_upload">
            <input type="hidden" name="action" value="upload_custom_file">
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
    <div id="uploadStatus"></div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

<script>
$(document).ready(function() {
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
            return; // 由于没有选择文件，无需进一步检查其他字段
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
</script>

<?php
get_footer(); // 获取网站底部
?>
