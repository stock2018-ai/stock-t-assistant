import requests
import datetime
import pandas as pd
import ta

print("智能做T助手 V2.5 启动")
print("时间:", datetime.datetime.now())

# =====================
# 1. 实时行情
# =====================

code = "sh600118"

url = f"https://qt.gtimg.cn/q={code}"

real = requests.get(url).text

real = real.replace('"','').replace(';','')

rt = real.split("~")

name = rt[1]
stock_code = rt[2]

current_price = float(rt[3])
yesterday = float(rt[4])
high = float(rt[33])
low = float(rt[34])
change = float(rt[32])


# =====================
# 2. 历史K线
# =====================

k_url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600118,day,,,60,qfq"

data = requests.get(k_url).json()

klines = data["data"]["sh600118"]["qfqday"]

df = pd.DataFrame(
    klines,
    columns=["date","open","close","high","low","volume"]
)

df["close"] = df["close"].astype(float)

# 均线
df["MA5"] = df["close"].rolling(5).mean()
df["MA10"] = df["close"].rolling(10).mean()

# RSI
rsi = ta.momentum.RSIIndicator(
    df["close"],
    window=14
)

df["RSI"] = rsi.rsi()

latest = df.iloc[-1]


# =====================
# 输出
# =====================

print("----------------")
print("股票:", name)
print("代码:", stock_code)

print("当前价格:", current_price)
print("昨日收盘:", yesterday)
print("今日涨跌:", change,"%")

print("今日最高:", high)
print("今日最低:", low)

print("----------------")

print("MA5:", round(latest["MA5"],2))
print("MA10:", round(latest["MA10"],2))
print("RSI:", round(latest["RSI"],2))

print("----------------")


# =====================
# 做T判断
# =====================

if latest["RSI"] < 35 and current_price < latest["MA5"]:
    print("🟢 低吸观察：RSI偏低，价格低于MA5")

elif latest["RSI"] > 70 and current_price > latest["MA5"]:
    print("🔴 高抛观察：RSI偏高，注意回调")

elif current_price < latest["MA10"]:
    print("🟡 弱势区域，等待止跌确认")

else:
    print("🟡 趋势观察")
