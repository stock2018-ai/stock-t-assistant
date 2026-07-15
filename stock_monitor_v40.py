import re
import json
import pandas as pd
import requests
import datetime


# =========================
# 智能做T助手 V3.2
# 基础框架
# =========================

print("智能做T助手 V3.2 稳定版")

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
# =========================
# V3.2.5 智能评分 + 做T策略
# =========================


score = 50


# 均线评分

if price > ma5:
    score += 10

if ma5 > ma10:
    score += 10


# RSI评分

if rsi_now < 40:
    score += 15


# 价格位置判断

print()

print("----------------")

print("智能评分:",
      score)


print("----------------")


print("操作建议:")


if score >= 80:

    print("🟢 偏积极")
    print("可关注低吸机会")


elif score >= 60:

    print("🟡 等待确认")


else:

    print("🔴 控制仓位")


print()

print("智能做T计划")


# 支撑区域判断

if price < level618:

    print("⚠️ 跌破0.618支撑")
    print("状态：调整偏弱")
    print("策略：等待止跌确认")


elif price <= level618 * 1.03:

    print("🟢 接近0.618支撑区域")
    print("关注低吸机会")


elif price <= level500:

    print("🟡 反弹区域")
    print("等待方向选择")


else:

    print("🔴 接近压力区域")
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
# =========================
# V3.3 底部/顶部趋势判断
# =========================


bottom_score = 0

top_risk = 0



# 1. RSI判断

if rsi_now < 35:

    bottom_score += 20


elif rsi_now < 45:

    bottom_score += 10


elif rsi_now > 75:

    top_risk += 20



# 2. 均线判断

if price < ma5 and price < ma10:

    bottom_score += 10


if ma5 > ma10:

    bottom_score += 10


if price > ma5 and price > ma10:

    top_risk += 10



# 3. 黄金分割位置判断

if price <= level618 * 1.03:

    bottom_score += 20


if price > level382:

    top_risk += 15



# 4. 距离波段高点

drawdown = (high_price-price)/high_price


if drawdown > 0.20:

    bottom_score += 15


if drawdown < 0.05:

    top_risk += 15



# 输出

print()

print("----------------")

print("趋势位置判断")


print("底部评分:",
      bottom_score)


print("顶部风险:",
      top_risk)



# 综合判断

if bottom_score >= 50:

    print("🟢 接近底部区域")

    print("策略: 等待企稳，可分批关注")


elif top_risk >= 40:

    print("🔴 高位风险区域")

    print("策略: 注意回调风险")


else:

    print("🟡 中间震荡区域")

    print("策略: 等待方向确认")

# =========================
# V3.3.1 成交量行为分析
# =========================


volume = data["volume"]


# 最近5日平均成交量

vol_ma5 = volume.rolling(5).mean().iloc[-1]


current_volume = float(volume.iloc[-1])


volume_ratio = current_volume / vol_ma5



print()

print("----------------")

print("成交量分析")


print("当前成交量:",
      round(current_volume/10000,2),
      "万")


print("5日均量:",
      round(float(vol_ma5)/10000,2),
      "万")


print("量比:",
      round(volume_ratio,2))


# 成交量判断

volume_score = 0


if volume_ratio < 0.7:

    print("🟢 缩量调整")

    print("抛压减弱")

    volume_score += 10



elif volume_ratio > 1.5:

    print("🔴 放量波动")

    print("注意资金博弈")


else:

    print("🟡 成交量正常")


# 上涨放量

if price > ma5 and volume_ratio > 1.2:

    print("🟢 放量上涨")

    volume_score += 10



# 下跌放量

if price < ma5 and volume_ratio > 1.5:

    print("⚠️ 下跌放量")

    print("短线压力增加")

    volume_score -= 10



print()

print("成交量评分:",
      volume_score)

# =========================
# V3.3.2 MACD趋势分析
# =========================


# EMA计算

ema12 = close.ewm(span=12).mean()

ema26 = close.ewm(span=26).mean()


dif = ema12 - ema26

dea = dif.ewm(span=9).mean()

macd = (dif - dea) * 2


dif_now = float(dif.iloc[-1])
dea_now = float(dea.iloc[-1])
macd_now = float(macd.iloc[-1])


print()

print("----------------")
print("MACD趋势分析")


print("DIF:",
      round(dif_now,3))

print("DEA:",
      round(dea_now,3))

print("MACD:",
      round(macd_now,3))


# 金叉判断

if dif_now > dea_now:

    print("🟢 MACD偏强")

else:

    print("🔴 MACD偏弱")


# =========================
# 简单底背离检测
# =========================


price_recent = close.tail(20)

macd_recent = macd.tail(20)


price_low1 = price_recent.iloc[:10].min()
price_low2 = price_recent.iloc[10:].min()


macd_low1 = macd_recent.iloc[:10].min()
macd_low2 = macd_recent.iloc[10:].min()



print()

if price_low2 < price_low1 and macd_low2 > macd_low1:

    print("🟢 发现MACD底背离")

    print("下跌动能减弱")

else:

    print("⚪ 暂未发现明显底背离")


print("----------------")
print("----------------")
print("----------------")
# =========================
# V3.4 综合交易判断
# =========================


total_score = 50


# 底部评分

total_score += bottom_score


# 成交量评分

total_score += volume_score



# MACD趋势

if dif_now > dea_now:

    total_score += 10

else:

    total_score -= 5



# 顶部风险扣分

total_score -= top_risk



# 限制范围

if total_score > 100:

    total_score = 100


if total_score < 0:

    total_score = 0



print()

print("================")

print("综合交易判断")


print("综合评分:",
      total_score)



print("底部评分:",
      bottom_score)


print("顶部风险:",
      top_risk)



print("成交量评分:",
      volume_score)



print()


# 最终结论


if total_score >= 80:

    print("🟢 强势关注区域")

    print("策略: 可考虑分批关注")


elif total_score >= 60:

    print("🟡 调整观察区域")

    print("策略: 等待确认")


else:

    print("🔴 风险区域")

    print("策略: 控制仓位")



print("================")


print("V3.4运行完成")
# =========================
# V4.0 AI综合分析报告
# =========================

print()
print("========================")
print("AI综合分析报告")
print("========================")

print("股票:", name)
print("当前价格:", round(price,2))

print()

# 趋势判断

if price > ma5 and ma5 > ma10:
    trend = "🟢 短期趋势向上"

elif price < ma5 and ma5 < ma10:
    trend = "🔴 短期趋势偏弱"

else:
    trend = "🟡 震荡观察"

print("趋势:", trend)


# 底部区域判断

if price <= level618 * 1.03:
    print("位置判断: 🟢 接近0.618支撑区域")

elif price <= level500:
    print("位置判断: 🟡 回调区域")

else:
    print("位置判断: 🔴 偏高区域")


# 简单AI建议

print()

if score >= 80:

    print("AI建议:")
    print("🟢 可以重点关注，等待确认信号")

elif score >= 60:

    print("AI建议:")
    print("🟡 保持观察，等待趋势确认")

else:

    print("AI建议:")
    print("🔴 控制仓位，注意风险")


print("========================")
# ==========================
# V4.0 AI综合评分
# ==========================

print()
print("================")
print("AI综合分析")
print("================")

ai_score = 50


# 1. 趋势评分

if price > ma5 and ma5 > ma10:
    ai_score += 20
    trend = "短期趋势向上"

elif price < ma5 and ma5 < ma10:
    ai_score -= 10
    trend = "短期趋势偏弱"

else:
    trend = "震荡观察"


# 2. 黄金分割位置

if price <= level618 * 1.03:
    ai_score += 15
    position = "接近0.618支撑区域"

elif price <= level500:
    ai_score += 5
    position = "回调区域"

else:
    ai_score -= 5
    position = "偏高区域"


# 3. MACD

if macd_value > 0:
    ai_score += 10
    macd_state = "MACD偏强"

else:
    ai_score -= 5
    macd_state = "MACD偏弱"


# 限制范围

if ai_score > 100:
    ai_score = 100

if ai_score < 0:
    ai_score = 0


# 底部概率

bottom_probability = ai_score


# 顶部风险

top_risk = 100 - ai_score


print("AI评分:", ai_score, "/100")

print()

print("趋势:", trend)

print("位置:", position)

print(macd_state)

print()

print("底部概率:",
      bottom_probability,
      "%")

print("顶部风险:",
      top_risk,
      "%")


print()

if ai_score >= 80:

    print("AI结论:")
    print("🟢 趋势较强，可重点关注")

elif ai_score >= 60:

    print("AI结论:")
    print("🟡 调整观察，等待确认")

else:

    print("AI结论:")
    print("🔴 趋势偏弱，注意风险")


print("================")
print("V3.3运行完成")
