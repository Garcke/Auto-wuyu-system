import cv2
from pyzbar.pyzbar import decode
import urllib.parse
import json
import re
import os
import numpy as np

def decode_qrcode(image_path: str):
    """
    读取图像，解码二维码，并提取二维码数据。
    """
    # 打印文件路径
    print(f"正在处理文件: {image_path}")

    # 将文件路径转换为 Unicode 格式
    image_path = os.path.abspath(image_path)

    # 读取图像文件为字节流
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # 将字节流转换为 numpy 数组
    image_array = np.frombuffer(image_bytes, np.uint8)

    # 使用 cv2.imdecode 解码图像
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # 检查图像是否成功读取
    if img is None:
        print(f"无法读取图像文件: {image_path}")
        return None

    # 解码二维码
    detected_barcodes = decode(img)

    # 遍历解码的二维码
    for barcode in detected_barcodes:
        # 提取二维码的边界框位置
        rect = barcode.rect
        cv2.rectangle(img, (rect.left, rect.top),
                      (rect.left + rect.width, rect.top + rect.height),
                      color=(0, 255, 0), thickness=2)

        # 解码数据
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # 显示解码结果
        print(f"二维码数据: {barcode_data}, 类型: {barcode_type}")

        # 在图像上绘制文本
        cv2.putText(img, barcode_data, (rect.left, rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 返回二维码数据
    return barcode_data

def extract_params(url: str):
    """
    解析 URL，并提取 rd 参数的内容，解码并提取 seqCode 和 hash。
    """
    # 解析 URL
    parsed_url = urllib.parse.urlparse(url)

    # 提取查询参数部分
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # 获取 rd 参数并进行解码
    rd_param = query_params.get('rd')[0]  # rd参数值
    decoded_rd_param = urllib.parse.unquote(rd_param)  # 解码

    print("Decoded rd param:", decoded_rd_param)

    # 使用正则表达式提取 seqCode 和 hash
    seq_code_match = re.search(r'seqCode=({.*?})', decoded_rd_param)
    hash_match = re.search(r'hash=([a-fA-F0-9]{32})', decoded_rd_param)

    # 检查是否匹配成功
    if seq_code_match and hash_match:
        # 提取 seqCode 和 hash
        seq_code = seq_code_match.group(1)
        hash_value = hash_match.group(1)

        # 将 seqCode 从 JSON 字符串转换为 Python 字典
        seq_code_dict = json.loads(seq_code)

        # 提取 transcriptId
        transcript_id = seq_code_dict.get('transcriptId')

        print("Transcript ID:", transcript_id)
        print("Hash:", hash_value)
        return transcript_id, hash_value
    else:
        print("无法匹配到 seqCode 或 hash")
        return None, None