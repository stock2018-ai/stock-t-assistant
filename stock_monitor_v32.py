import re
import json
import pandas as pd
import requests
import datetime


# =========================
# 智能做T助手 V3.2
# 基础框架
# =========================

print("智能做T助手 V3.2")

print("时间:", datetime.datetime.now())
print("----------------")


# 股票设置

stock = "600118"
name = "中国卫星"


# =========================
# 获取新浪A股K线数据
# =========================

code = "sh600118"


url = (
    "https://quotes.sina.cn/cn/api/jsonp_v2.php/"
    "var%20_data=/CN_MarketDataService.getKLineData"
    "?symbol="
    + code +
    "&scale=240"
    "&ma=no"
    "&datalen=120"
)


try:

    response = requests.get(
        url,
        timeout=10
    )

except Exception as e:

    print("行情获取失败:")
    print(e)
    exit()


text = response.text


try:

    data_list = json.loads(
        re.search(
            r'\((.*)\)',
            text
        ).group(1)
    )

except Exception:

    print("行情解析失败")
    exit()


if not data_list:

    print("没有获取到股票数据")
    exit()


# =========================
# 数据整理
# =========================

records = []


for item in data_list:

    records.append([

        item["day"],

        float(item["open"]),

        float(item["close"]),

        float(item["high"]),

        float(item["low"]),

        float(item["volume"])

    ])



data = pd.DataFrame(

    records,

    columns=[

        "date",
        "open",
        "close",
        "high",
        "low",
        "volume"

    ]

)


print("数据获取成功")
print("K线数量:", len(data))

print(data.tail())

print("----------------")
# =========================
# 技术指标计算
# V3.2 第二阶段
# =========================


close = data["close"]


# 当前价格

price = float(close.iloc[-1])


# =========================
# MA均线
# =========================

ma5 = close.rolling(5).mean().iloc[-1]

ma10 = close.rolling(10).mean().iloc[-1]


# =========================
# RSI指标
# =========================

delta = close.diff()


gain = delta.where(delta > 0, 0)

loss = -delta.where(delta < 0, 0)


avg_gain = gain.rolling(14).mean()

avg_loss = loss.rolling(14).mean()


rs = avg_gain / avg_loss


rsi = 100 - (100 / (1 + rs))


rsi_now = float(rsi.iloc[-1])


# =========================
# 输出
# =========================

print()

print("股票:", name)

print("代码:", stock)

print()

print("当前价格:",
      round(price,2))


print("----------------")


print("MA5:",
      round(float(ma5),2))


print("MA10:",
      round(float(ma10),2))


print("RSI:",
      round(rsi_now,2))


print("----------------")
# =========================
# V3.2 第三阶段
# 自动上涨波段 + 黄金分割
# =========================


# 最近120根K线

recent = close.tail(120)


# 波段最低点

low_price = float(recent.min())
# =========================
# V3.2.4 智能上涨波段识别
# =========================


recent = close.tail(120)


# 最近20日寻找启动低点

window = 20

rolling_low = recent.rolling(window).min()


start_index = rolling_low.idxmin()


low_price = float(recent.loc[start_index])


# 启动点之后寻找最高价

after_start = recent.loc[start_index:]


high_price = float(after_start.max())


# 如果异常，退回最近波段

if high_price <= low_price:

    low_price = float(recent.min())

    high_price = float(recent.max())


wave_gain = (high_price-low_price)/low_price



# 黄金分割

level382 = high_price - (high_price-low_price)*0.382

level500 = high_price - (high_price-low_price)*0.5

level618 = high_price - (high_price-low_price)*0.618



print()

print("----------------")

print("智能波段识别")


print("启动低点:",
      round(low_price,2))


print("上涨高点:",
      round(high_price,2))


print("上涨幅度:",
      round(wave_gain*100,2),
      "%")


print()

print("黄金分割")


print("0.382压力位:",
      round(level382,2))


print("0.5关键位:",
      round(level500,2))


print("0.618支撑:",
      round(level618,2))


print("----------------")

print()

print("----------------")

print("黄金分割")


print("分析周期: 最近120日")


print("波段低点:",
      round(low_price,2))


print("波段高点:",
      round(high_price,2))


print("上涨幅度:",
      round(wave_gain*100,2),
      "%")


print()

print("0.382压力位:",
      round(level382,2))


print("0.5关键位:",
      round(level500,2))


print("0.618支撑:",
      round(level618,2))


print("----------------")
