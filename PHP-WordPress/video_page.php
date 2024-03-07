<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Video Page</title>
</head>
<body>
    <?php
    $videoUrl = $_GET['videoUrl'];
    //$videoUrl
    $videoUrl = isset($_GET['videoUrl']) ? $_GET['videoUrl'] : '';
    //$decodedUrl = urldecode($videoUrl);
    //error_log('ssssssssssss', $videoUrl);
    //var_dump($videoUrl); // 这行代码会打印$videoUrl的值
    //经过找专家，这个页面要放到网站根目录中，不能放到插件内部。
    ?>
    <div>wwwroot</div>
    <video width="100%" controls>
        <source src="<?php echo $videoUrl; ?>" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <!-- 在这里添加更多视频详细信息 -->
</body>
</html>

