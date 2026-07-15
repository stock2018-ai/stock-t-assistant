import requests
import datetime

print("智能做T助手启动")
print("时间:", datetime.datetime.now())

code = "sh600118"

url = f"https://qt.gtimg.cn/q={code}"

response = requests.get(url)

data = response.text

print("股票数据:")
print(data)

print("监控股票：中国卫星 600118")
