# @-*- coding = utf-8 _*_
# @Time : 2024/6/2 2:44
# @Author : 杨昌军
# @File : mjc-scrapy.py
# @Software : PyCharm


import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 读取JSON文件
with open('getSs.json', 'r', encoding='utf-8') as file:
    regions = json.load(file)

base_url = "https://yz.chsi.com.cn/zsml/querySchAction.do"

# 定义个性化请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': 'JSESSIONID=CD02A8ED39F4ED15F1974C1FC024B76C; CHSICC_CLIENTFLAGZSML=d9dc52d66da51bbfa609875459174e30; CHSICC01=!wbmiHNrCDQdJbtAnVPBkiJOoJxwY2hlOdAHeiR8kvaDjvLvCK56r82wL5U05LUkvyBMt+VJfPTunXA==; Hm_lvt_3916ecc93c59d4c6e9d954a54f37d84c=1717262175; _gid=GA1.3.1157368183.1717262175; JSESSIONID=06E22463560A5BB36554C03C957B3368; XSRF-CCKTOKEN=2c1db769e3e93e753dcdcecc0289ec4a; CHSICC_CLIENTFLAGYZ=5d9a178e980046720dfb5abc37a90f32; Hm_lpvt_3916ecc93c59d4c6e9d954a54f37d84c=1717265564; _ga=GA1.3.1818371210.1681481341; _ga_YZV5950NX3=GS1.1.1717262175.5.1.1717268484.0.0.0',
}


# 循环构建URL并发送请求
for region in regions:
    ssdm = region["dm"]
    params = {
        'ssdm': ssdm,
        'dwmc': '北京大学',  # 示例中使用的固定值
        'mldm': '',
        'mlmc': '',
        'yjxkdm': '0552',  # 示例中使用的固定值
        'xxfs': '',
        'zymc': ''
    }

    try:
        response = requests.get(base_url, headers=headers, params=params, verify=False)

        # 检查请求是否成功
        if response.status_code == 200:
            # 处理响应内容
            print(f"Successfully retrieved data for region code {ssdm}")
            # 可以在这里解析和处理响应内容
        else:
            print(f"Failed to retrieve data for region code {ssdm}, status code: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"SSL error for region code {ssdm}: {e}")

