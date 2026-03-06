import requests

url = "https://httpbin.org/get"

resp = requests.get(url, params={"name": "侯金双", "city": "广东"})

print("状态码：", resp.status_code)
print("响应正文：", resp.text)
print("响应头：", resp.url) 
