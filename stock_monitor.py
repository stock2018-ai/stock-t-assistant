import requests
import datetime

print("智能做T助手启动")
print("运行时间:", datetime.datetime.now())

# 中国卫星 股票代码
code = "sh600118"

url = f"https://qt.gtimg.cn/q={code}"

data = requests.get(url).text

print(data)

if data:
    print("正在监控：中国卫星 600118")
    print("行情获取成功")
else:
    print("行情获取失败")
