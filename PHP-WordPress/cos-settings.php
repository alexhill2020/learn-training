<?php

add_action('admin_menu', 'wp_cos_integration_add_settings_page');

function wp_cos_integration_add_settings_page() {
    add_options_page(
        '腾讯云COS对象存储仓库设置', // 页面标题
        '对象存储仓库', // 菜单标题
        'manage_options', // 所需能力
        'wp-cos-integration-settings', // 菜单slug
        'wp_cos_integration_settings_page' // 显示设置页面的函数
    );
}


function wp_cos_integration_settings_page() {
    ?>
    <div class="wrap">
        <h2>腾讯云COS对象存储仓库 - 设置</h2>
        <form method="post" action="options.php">
            <?php
            settings_fields('wp_cos_integration_settings_group');
            do_settings_sections('wp-cos-integration-settings');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}


//还未做表单验证逻辑，应补上，即输入为空或不为指定格式，则提交不成功，并提示用户。


add_action('admin_init', 'wp_cos_integration_register_settings');

function wp_cos_integration_register_settings() {
    // 注册设置组
    register_setting('wp_cos_integration_settings_group', 'wp_cos_integration_settings');

    // 添加设置区域
    add_settings_section(
        'wp_cos_integration_settings_section', 
        '基本设置', 
        'wp_cos_integration_settings_section_callback', 
        'wp-cos-integration-settings'
    );

    // 添加cos_bucket设置字段
    add_settings_field(
        'wp_cos_integration_cos_bucket', 
        '存储桶名称', 
        'wp_cos_integration_cos_bucket_callback', 
        'wp-cos-integration-settings', 
        'wp_cos_integration_settings_section'
    );
    
    // 添加cos_region设置字段
    add_settings_field(
        'wp_cos_integration_cos_region', 
        '所属地域', 
        'wp_cos_integration_cos_region_callback', 
        'wp-cos-integration-settings', 
        'wp_cos_integration_settings_section'
    );

    // 添加SecretID设置字段
    add_settings_field(
        'wp_cos_integration_secret_id', 
        'SecretID', 
        'wp_cos_integration_secret_id_callback', 
        'wp-cos-integration-settings', 
        'wp_cos_integration_settings_section'
    );

    // 添加SecretKey设置字段
    add_settings_field(
        'wp_cos_integration_secret_key', 
        'SecretKey', 
        'wp_cos_integration_secret_key_callback', 
        'wp-cos-integration-settings', 
        'wp_cos_integration_settings_section'
    );
}

function wp_cos_integration_settings_section_callback() {
    echo '<p>请访问你的<a href="https://console.cloud.tencent.com/" target="_blank"><b> 腾讯云控制台 </b></a>获取存储桶名称、所属地域、SecretID、SecretKey等信息。</br><b><span style="color: red;">在输入时请仔细核对，确保全部信息（包括字母大小写）输入准确无误，否则会交互不成功。</span></b></p>';
}

function wp_cos_integration_cos_bucket_callback() {
    $options = get_option('wp_cos_integration_settings');
    echo "<input type='text' name='wp_cos_integration_settings[cos_bucket]' value='" . esc_attr($options['cos_bucket']) . "' />";
    echo "<p>输入的存储桶名称应为“ad-xxxxxxxxxx”格式，“x”为数字，共10位。</p>";
}

function wp_cos_integration_cos_region_callback() {
    $options = get_option('wp_cos_integration_settings');
    echo "<input type='text' name='wp_cos_integration_settings[cos_region]' value='" . esc_attr($options['cos_region']) . "' />";
    echo "<p>输入的所属地域应为“ap-chongqing”格式。</p>";
}

function wp_cos_integration_secret_id_callback() {
    $options = get_option('wp_cos_integration_settings');
    echo "<input type='text' style='width: 350px;' name='wp_cos_integration_settings[secret_id]' value='" . esc_attr($options['secret_id']) . "' />";
    echo "<p>输入的SecretID应为36位，只能包含大写字母、小写字母和数字，不能有中文或其它字符。</p>";
}

function wp_cos_integration_secret_key_callback() {
    $options = get_option('wp_cos_integration_settings');
    $secretKeyIsSet = !empty($options['secret_key']);
    echo "<input type='text' style='width: 350px;' name='wp_cos_integration_settings[secret_key]' value='" . ($secretKeyIsSet ? "********************************" : "") . "' />";
    echo "<p>输入的SecretKey应为32位，只能包含大写字母、小写字母和数字，不能有中文或其它字符。</p>";
    if ($secretKeyIsSet) {
        echo "<p><b>SecretKey 已设置。留空此字段以保持不变，或输入新值以更新。</b></p>";
    }
}
