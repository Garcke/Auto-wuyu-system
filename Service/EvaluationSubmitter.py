import requests

def submit_evaluation(transcript_id: str, hash_value: str, token: str):
    """
    提交评估数据到指定 URL。
    """
    url = "http://27.37.67.47/admin/ReflectionMeeting/submitEvaluationForm"

    headers = {
        "Authorization": f"Bearer {token}",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    # 使用占位符构建请求体数据
    data = {
        "seqCode": f"{{\"formType\":\"ClassmatesEvaluation\",\"transcriptId\":{transcript_id}}}",
        "formData": "{\"morality\":80,\"intelligence\":80,\"physique\":80,\"aesthetics\":80,\"labour\":80}",
        "hash": hash_value
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 打印响应状态码和内容
    print(response.status_code)
    print(response.text)