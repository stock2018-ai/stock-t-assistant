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


# V3.1.2 波段识别黄金分割

# V3.1.4 智能波段识别
# V3.1.5 智能上涨波段识别


recent = close.tail(120)


# 找最近上涨启动点

rolling_low = recent.rolling(20).min()

start_price = float(rolling_low.min())


# 找启动点之后最高价

start_index = rolling_low.idxmin()


after_start = recent.loc[start_index:]


end_price = float(after_start.max())


# 如果涨幅不足20%，使用最近波段

if (end_price-start_price)/start_price < 0.2:

    start_price = float(recent.min())
    end_price = float(recent.max())


low_price = start_price
high_price = end_price


wave_gain = (high_price-low_price)/low_price


# 如果最高点在最低点之后
# 计算上涨波段回调

level382 = high_price - (high_price-low_price)*0.382
level500 = high_price - (high_price-low_price)*0.5
level618 = high_price - (high_price-low_price)*0.618


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

print("分析波段")

print("波段低点:",
      round(low_price,2))

print("波段高点:",
      round(high_price,2))


print("涨幅:",
      round((high_price-low_price)/low_price*100,2),
      "%")


print("0.382压力位:",
      round(level382,2))

print("0.5关键位:",
      round(level500,2))

print("0.618支撑:",
      round(level618,2))


# 简单评分

score = 50


if price > ma5:
    score +=10

if ma5 > ma10:
    score +=10

if rsi_now < 40:
    score +=15

if price < level618:

    print("⚠️ 跌破0.618支撑")
    print("等待止跌确认")

elif price <= level618*1.03:

    print("🟢 接近0.618支撑")
    print("关注低吸机会")
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

if price < level618:

    print("⚠️ 跌破0.618支撑")
    print("状态：调整偏弱")
    print("策略：等待止跌确认")

elif price <= level618 * 1.03:

    print("🟢 0.618附近")
    print("状态：观察低吸机会")

elif price <= level500:

    print("🟡 反弹区域")
    print("等待方向选择")

else:

    print("🔴 接近压力")
    print("考虑高抛做T")




print()

print("参考买入区:",
      round(level618,2),
      "-",
      round(level618*1.03,2))


print("参考卖T区:",
      round(level500,2),
      "-",
      round(level382,2))
print("----------------")
print("V3.1运行完成")
