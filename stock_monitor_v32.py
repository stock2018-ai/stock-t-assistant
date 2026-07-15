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
