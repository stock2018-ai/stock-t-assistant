import requests
import datetime
import pandas as pd
import ta

print("智能做T助手 V2 启动")
print("时间:", datetime.datetime.now())

# 中国卫星
code = "600118"

# 腾讯历史K线接口
url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh{code},day,,,60,qfq"

data = requests.get(url).json()

klines = data["data"]["sh600118"]["qfqday"]

df = pd.DataFrame(
    klines,
    columns=["date","open","close","high","low","volume"]
)

df["close"] = df["close"].astype(float)

# MA
df["MA5"] = df["close"].rolling(5).mean()
df["MA10"] = df["close"].rolling(10).mean()

# RSI
rsi = ta.momentum.RSIIndicator(
    df["close"],
    window=14
)

df["RSI"] = rsi.rsi()

latest = df.iloc[-1]

print("----------------")
print("股票：中国卫星 600118")
print("收盘价:", latest["close"])
print("MA5:", round(latest["MA5"],2))
print("MA10:", round(latest["MA10"],2))
print("RSI:", round(latest["RSI"],2))
print("----------------")


if latest["RSI"] < 30:
    print("🟢 RSI超卖，关注低吸机会")

elif latest["RSI"] > 70:
    print("🔴 RSI偏高，注意回调")

else:
    print("🟡 RSI正常，等待趋势")
# 简单做T提示
# 做T综合判断

if latest["RSI"] < 30 and latest["close"] < latest["MA5"]:
    print("🟢 RSI超卖 + 跌破MA5，关注低吸机会")

elif latest["RSI"] > 70 and latest["close"] > latest["MA5"]:
    print("🔴 RSI高位 + 远离MA5，注意高抛机会")

else:
    print("🟡 趋势中，等待更明确机会")
