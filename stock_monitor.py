import requests
import datetime

print("智能做T助手启动")
print("时间:", datetime.datetime.now())

# 股票：600118 中国卫星
code = "sh600118"

url = f"https://qt.gtimg.cn/q={code}"

data = requests.get(url).text

# 去掉前后无用字符
data = data.replace('"', '').replace(';', '')

# 按 ~ 分割
items = data.split("~")

name = items[1]
code = items[2]
price = float(items[3])
yesterday = float(items[4])
change = float(items[32])
high = float(items[33])
low = float(items[34])

print("----------------")
print("股票:", name)
print("代码:", code)
print("当前价格:", price)
print("昨日收盘:", yesterday)
print("涨跌幅:", change, "%")
print("今日最高:", high)
print("今日最低:", low)
print("----------------")

# 简单做T提示
if change <= -3:
    print("提示：今日大跌，关注低吸机会")
elif change >= 3:
    print("提示：今日上涨，关注高抛机会")
else:
    print("提示：等待趋势确认")
