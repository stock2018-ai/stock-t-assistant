import requests
import datetime
import pandas as pd
import ta

print("智能做T助手 V3 启动")
print("时间:", datetime.datetime.now())


# =====================
# 实时行情
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
change = float(rt[32])


# =====================
# 历史K线
# =====================

k_url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600118,day,,,120,qfq"

data = requests.get(k_url).json()

klines = data["data"]["sh600118"]["qfqday"]


df = pd.DataFrame(
    klines,
    columns=["date","open","close","high","low","volume"]
)


for col in ["close","high","low","volume"]:
    df[col] = df[col].astype(float)


# 均线

df["MA5"] = df["close"].rolling(5).mean()
df["MA10"] = df["close"].rolling(10).mean()


# RSI

df["RSI"] = ta.momentum.RSIIndicator(
    df["close"],
    window=14
).rsi()


# 成交量均值

df["VOL5"] = df["volume"].rolling(5).mean()


latest = df.iloc[-1]


# =====================
# 0.618黄金分割
# =====================

high_price = df["high"].max()
low_price = df["low"].min()

support_618 = high_price - (high_price-low_price)*0.618


# 成交量变化

volume_change = (
    latest["volume"] / latest["VOL5"] - 1
) * 100



# =====================
# 输出
# =====================

print("----------------")
print("股票:", name)
print("代码:", stock_code)

print("当前价格:", current_price)
print("今日涨跌:", change,"%")

print("----------------")

print("MA5:", round(latest["MA5"],2))
print("MA10:", round(latest["MA10"],2))
print("RSI:", round(latest["RSI"],2))

print("0.618支撑:",
      round(support_618,2))

print("成交量变化:",
      round(volume_change,2),
      "%")

print("----------------")


# =====================
# 做T判断
# =====================

score = 0


if current_price <= support_618*1.03:
    score += 1
    print("✔ 接近0.618支撑")


if latest["RSI"] < 35:
    score += 1
    print("✔ RSI偏低")


if volume_change < 0:
    score += 1
    print("✔ 缩量调整")


print("----------------")

print("做T评分:", score,"/3")


if score >= 2:
    print("🟢 关注低吸机会")

elif change > 5:
    print("🔴 注意高抛")

else:
    print("🟡 等待确认")
