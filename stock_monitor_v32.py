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
print("我是V3.2测试文件")
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
