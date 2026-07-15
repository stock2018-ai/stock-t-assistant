import yfinance as yf
import pandas as pd
import datetime


# 股票设置
stock = "600118.SS"
name = "中国卫星"


print("智能做T助手 V3.1")
print("时间:", datetime.datetime.now())
print("----------------")


# 获取数据
data = yf.download(
    stock,
    period="6mo",
    interval="1d"
)


close = data["Close"]
close = close.squeeze()

price = float(close.iloc[-1])


# 均线
ma5 = close.rolling(5).mean().iloc[-1]
ma10 = close.rolling(10).mean().iloc[-1]


# RSI
delta = close.diff()

gain = delta.where(delta > 0,0)
loss = -delta.where(delta < 0,0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

rsi = 100 - (100/(1+rs))

rsi_now = float(rsi.iloc[-1])


# 黄金分割

high = float(close.max())
low = float(close.min())

level618 = low + (high-low)*0.618
level500 = low + (high-low)*0.5
level382 = low + (high-low)*0.382


print("股票:",name)
print("代码:",stock)
print()

print("当前价格:",round(price,2))

print("----------------")
print("MA5:",round(float(ma5),2))
print("MA10:",round(float(ma10),2))
print("RSI:",round(rsi_now,2))


print("----------------")
print("黄金分割")

print("半年最高:",
      round(high,2))

print("半年最低:",
      round(low,2))


print("0.618支撑:",
      round(level618,2))

print("0.5支撑:",
      round(level500,2))

print("0.382支撑:",
      round(level382,2))


# 简单评分

score = 50


if price > ma5:
    score +=10

if ma5 > ma10:
    score +=10

if rsi_now < 40:
    score +=15

if price < level618:
    score +=10


print("----------------")
print("智能评分:",
      score)


print("----------------")


if score >=80:
    print("操作建议：")
    print("🟢 偏积极，可考虑低吸")

elif score >=60:
    print("操作建议：")
    print("🟡 等待确认")

else:
    print("操作建议：")
    print("🔴 控制仓位")


print("----------------")
print("V3.1运行完成")
