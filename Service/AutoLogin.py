import os
import base64
import json
import requests
import ddddocr

def get_captcha_img():
    """
    获取验证码图片和对应的uuid
    """
    cap_url = 'http://27.37.67.47/admin/captchaImage'
    res = requests.get(cap_url)
    res_js = res.json()
    img_b64 = res_js['img']
    uuid = res_js['uuid']
    cap_code = recognize_captcha(img_b64)
    return uuid, cap_code

def recognize_captcha(img_b64):
    """
    识别验证码
    """
    # 解码 Base64 字符串为字节数据
    image_bytes = base64.b64decode(img_b64)

    # 创建 OCR 对象并进行识别
    ocr = ddddocr.DdddOcr()
    result = ocr.classification(image_bytes)
    return result

def post_login(username, password, uuid, cap_code):
    """
    登录验证
    """
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    login_url = 'http://27.37.67.47/admin/login'
    data = {"code": f"{cap_code}",
            "password": f"{password}",
            "username": f"{username}",
            "uuid": f"{uuid}"}
    res = requests.post(login_url, data=json.dumps(data), headers=headers)
    res_js = res.json()

    print(res_js)
    if res_js['code'] == 200:
        print('登录成功！')
    else:
        print('登录失败！')
    return res_js.get('token')

def load_config():
    """
    加载配置文件
    """
    config_path = os.path.join(os.path.dirname(__file__), 'userconfig.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

if __name__ == '__main__':
    config = load_config()
    username = config['username']
    password = config['password']
    uuid, cap_code = get_captcha_img()
    print(cap_code)
   