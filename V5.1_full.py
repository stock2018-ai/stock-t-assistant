# ==========================
# V5.1_full 智能交易助手
# Part 1
# 基础框架 + Gmail + 行情
# ==========================

import re
import json
import pandas as pd
import requests
import datetime
import os
import smtplib

from email.mime.text import MIMEText


# ==========================
# 程序启动
# ==========================

print("==========================")
print("V5.1_full 智能交易助手")
print("==========================")

print("运行时间:",
      datetime.datetime.now())


# ==========================
# 股票设置
# ==========================

stock_code = "600118"

stock_name = "中国卫星"

sina_code = "sh600118"
name = stock_name
stock = stock_code

# ==========================
# Gmail发送函数
# ==========================

def send_email(subject, content):

    sender = os.getenv("GMAIL_USER")

    password = os.getenv("GMAIL_PASS")

    receiver = sender


    if not sender or not password:

        print("⚠️ 未配置Gmail账号")

        return



    msg = MIMEText(
        content,
        "plain",
        "utf-8"
    )


    msg["Subject"] = subject

    msg["From"] = sender

    msg["To"] = receiver



    try:

        server = smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        )


        server.login(
            sender,
            password
        )


        server.sendmail(
            sender,
            receiver,
            msg.as_string()
        )


        server.quit()


        print("📧 Gmail发送成功")


    except Exception as e:

        print("❌ Gmail发送失败")

        print(e)




# ==========================
# 获取新浪K线
# ==========================

print()
print("----------------")
print("获取行情数据")
print("----------------")



url = (

    "https://quotes.sina.cn/cn/api/jsonp_v2.php/"

    "var%20_data=/CN_MarketDataService.getKLineData"

    "?symbol="

    + sina_code

    + "&scale=240"

    "&ma=no"

    "&datalen=120"

)



try:

    response = requests.get(
        url,
        timeout=10
    )


except Exception as e:

    print("行情获取失败")

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

    print("没有行情数据")

    exit()



# ==========================
# 数据整理
# ==========================


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



print()

print("股票:",
      stock_name)

print("代码:",
      stock_code)

print()

print("K线数量:",
      len(data))


print(data.tail())


print("----------------")



# 当前价格

close = data["close"]

price = float(
    close.iloc[-1]
)


print()

print("当前价格:",
      round(price,2))


print("----------------")
# ==========================
# V5.1_full Part 2
# 技术指标 + AI评分
# ==========================


print()
print("================")
print("技术指标分析")
print("================")


# ==========================
# MA均线
# ==========================

ma5 = (
    close
    .rolling(5)
    .mean()
    .iloc[-1]
)


ma10 = (
    close
    .rolling(10)
    .mean()
    .iloc[-1]
)



print()

print("MA5:",
      round(float(ma5),2))


print("MA10:",
      round(float(ma10),2))





# ==========================
# RSI
# ==========================


delta = close.diff()


gain = delta.where(
    delta > 0,
    0
)


loss = -delta.where(
    delta < 0,
    0
)



avg_gain = (
    gain
    .rolling(14)
    .mean()
)



avg_loss = (
    loss
    .rolling(14)
    .mean()
)



rs = (
    avg_gain /
    avg_loss
)



rsi = (
    100 -
    (100/(1+rs))
)



rsi_now = float(
    rsi.iloc[-1]
)



print()

print("RSI:",
      round(rsi_now,2))





# ==========================
# MACD
# ==========================


ema12 = (
    close
    .ewm(span=12)
    .mean()
)


ema26 = (
    close
    .ewm(span=26)
    .mean()
)



dif = ema12 - ema26


dea = (
    dif
    .ewm(span=9)
    .mean()
)


macd = (
    dif-dea
)*2



dif_now = float(
    dif.iloc[-1]
)


dea_now = float(
    dea.iloc[-1]
)


macd_now = float(
    macd.iloc[-1]
)



print()

print("MACD:",
      round(macd_now,3))


if dif_now > dea_now:

    print(
        "🟢 MACD偏强"
    )

else:

    print(
        "🔴 MACD偏弱"
    )





# ==========================
# 成交量分析
# ==========================


print()

print("----------------")

print("成交量分析")



volume = data["volume"]



vol_ma5 = (
    volume
    .rolling(5)
    .mean()
    .iloc[-1]
)



current_volume = float(
    volume.iloc[-1]
)



volume_ratio = (
    current_volume /
    vol_ma5
)



print(
    "量比:",
    round(volume_ratio,2)
)



volume_score = 0



if volume_ratio < 0.7:


    print(
        "🟢 缩量调整"
    )

    volume_score += 10



elif volume_ratio > 1.5:


    print(
        "🔴 放量波动"
    )



else:


    print(
        "🟡 成交量正常"
    )





# ==========================
# AI综合评分
# ==========================


print()

print("================")

print("AI综合评分")

print("================")



ai_score = 50



# 趋势

if price > ma5:

    ai_score += 10


else:

    ai_score -= 5




if ma5 > ma10:

    ai_score += 10



# RSI

if rsi_now < 40:

    ai_score += 10


elif rsi_now > 70:

    ai_score -= 10




# MACD

if dif_now > dea_now:

    ai_score += 10

else:

    ai_score -= 5




# 成交量

ai_score += volume_score




# 限制

ai_score = max(
    0,
    min(
        100,
        ai_score
    )
)




print(
    "AI评分:",
    ai_score,
    "/100"
)



if ai_score >= 80:


    print(
        "🟢 强势关注区域"
    )


elif ai_score >= 60:


    print(
        "🟡 等待确认区域"
    )


else:


    print(
        "🔴 风险区域"
    )



print("================")
# ==========================
# V5.1_full Part 3
# V4.5上涨波 + V4.6交易计划
# ==========================


print()

print("================")
print("V4.5 最近上涨波分析")
print("================")



# 最近120根K线

wave = data.tail(120).reset_index(
    drop=True
)



# 找上涨波低点

low_index = wave["low"].idxmin()



wave_low = float(

    wave.loc[
        low_index,
        "low"
    ]

)



# 低点之后最高点

after_low = wave.iloc[
    low_index:
]



wave_high = float(

    after_low["high"].max()

)




print()

print("上涨波低点:",
      round(wave_low,2))


print("上涨波高点:",
      round(wave_high,2))





# 涨幅

wave_gain = (

    wave_high - wave_low

) / wave_low * 100




print()

print("上涨幅度:",
      round(wave_gain,2),
      "%")




# 当前回撤

drawdown = (

    wave_high-price

) / wave_high * 100




print("当前回撤:",
      round(drawdown,2),
      "%")





# ==========================
# 黄金分割
# ==========================


fib618 = wave_high - (

    wave_high-wave_low

) * 0.618



fib500 = wave_high - (

    wave_high-wave_low

) * 0.5



fib382 = wave_high - (

    wave_high-wave_low

) * 0.382





print()

print("黄金分割:")


print(
    "0.618:",
    round(fib618,2)
)


print(
    "0.5:",
    round(fib500,2)
)


print(
    "0.382:",
    round(fib382,2)
)



print("================")





# ==========================
# V4.6 智能交易计划
# ==========================


print()

print("================")
print("V4.6 智能交易计划")
print("================")




# 买入观察区


buy_low = wave_low

buy_high = fib618




print()

print(
    "观察买入区:",
    round(buy_low,2),
    "-",
    round(buy_high,2)
)





# 确认买点


confirm_buy = fib618



print()

print(
    "确认买点:",
    round(confirm_buy,2)
)






# ==========================
# 目标价格
# ==========================


target1 = fib500

target2 = fib382

target3 = wave_high





print()

print("目标价格:")



print(
    "第一目标:",
    round(target1,2)
)



print(
    "第二目标:",
    round(target2,2)
)



print(
    "前高目标:",
    round(target3,2)
)







# ==========================
# 风险控制
# ==========================


stop_loss = wave_low * 0.97




print()

print("风险控制:")


print(
    "防守位:",
    round(stop_loss,2)
)






# ==========================
# 当前状态
# ==========================


print()


if price <= fib618:


    print("当前状态:")

    print(
        "🟡 回调区域，等待止跌确认"
    )



elif price <= fib500:


    print("当前状态:")

    print(
        "🟢 支撑反弹观察"
    )



else:


    print("当前状态:")

    print(
        "🟠 接近压力区域"
    )



print("================")
# ==========================
# V5.1_full Part 4
# V4.7 + V5.1 邮件提醒
# ==========================


print()

print("================")
print("V4.7 邮件提醒")
print("================")



# ==========================
# 买入确认提醒
# ==========================


if price >= confirm_buy:


    email_title = (

        "【买入提醒】"

        + stock_name

        + "站稳关键位"

    )



    email_content = f"""

股票:
{stock_name}


代码:
{stock_code}


当前价格:
{round(price,2)}


确认买点:
{round(confirm_buy,2)}


状态:
🟢 已达到买入确认位


交易计划:

第一目标:
{round(target1,2)}

第二目标:
{round(target2,2)}

前高目标:
{round(target3,2)}


风险防守:
{round(stop_loss,2)}

"""



    print(email_content)



    send_email(

        email_title,

        email_content

    )



else:


    print(
        "暂未触发买入提醒"
    )







# ==========================
# V5.1 目标价格提醒
# ==========================


print()

print("================")
print("V5.1 目标提醒")
print("================")




if price >= target3:



    email_title = (

        "【突破前高提醒】"

        + stock_name

    )



    email_content = f"""

股票:
{stock_name}


当前价格:
{round(price,2)}


突破目标:
{round(target3,2)}


状态:
🚀 已突破前高


建议:
关注趋势延续

"""



    send_email(

        email_title,

        email_content

    )


    print(email_content)






elif price >= target2:



    email_title = (

        "【第二目标提醒】"

        + stock_name

    )



    email_content = f"""

股票:
{stock_name}


当前价格:
{round(price,2)}


第二目标:
{round(target2,2)}


状态:
🎯 第二目标达到


建议:
继续观察趋势

"""



    send_email(

        email_title,

        email_content

    )


    print(email_content)








elif price >= target1:



    email_title = (

        "【第一目标提醒】"

        + stock_name

    )



    email_content = f"""

股票:
{stock_name}


当前价格:
{round(price,2)}


第一目标:
{round(target1,2)}


状态:
🎯 第一目标达到


建议:
可考虑部分止盈

"""



    send_email(

        email_title,

        email_content

    )


    print(email_content)






else:


    print(
        "🟡 暂未达到目标价格"
    )





print()
# ==========================
# V5.2 防守位风险提醒
# ==========================

print()
print("================")
print("V5.2 风险提醒")
print("================")


if price <= stop_loss:

    email_title = (
        "【风险警报】"
        + name
        + "跌破防守位"
    )


    email_content = f"""
股票:
{name}

代码:
{stock}

当前价格:
{round(price,2)}

防守位:
{round(stop_loss,2)}

状态:
🔴 跌破风险控制线

建议:
停止加仓
重新评估趋势

交易计划:
观察止跌信号
"""


    send_email(
        email_title,
        email_content
    )


    print(email_content)


else:

    print("🟢 防守位正常，未触发风险提醒")


print("================")
print("================")
# ==========================
# V5.3 买入确认过滤
# ==========================

print()
print("================")
print("V5.3 买入确认")
print("================")


buy_confirm = False


# 条件1：价格突破确认位

if price >= confirm_buy:

    price_ok = True

else:

    price_ok = False



# 条件2：成交量确认

if volume_ratio >= 1:

    volume_ok = True

else:

    volume_ok = False



# 条件3：MACD确认

if dif_now > dea_now:

    macd_ok = True

else:

    macd_ok = False



# 综合判断

if price_ok and volume_ok and macd_ok:

    buy_confirm = True



if buy_confirm:


    email_title = (
        "【V5.3买入确认】"
        + name
    )


    email_content = f"""
股票:
{name}

代码:
{stock}

当前价格:
{round(price,2)}

确认买点:
{round(confirm_buy,2)}

成交量:
{round(volume_ratio,2)}

MACD:
强势

状态:
🟢 三重确认通过

建议:
可考虑分批关注
"""


    send_email(
        email_title,
        email_content
    )


    print(email_content)



else:

    print("🟡 未满足买入三重确认")


    print(
        "价格:",
        price_ok,
        "成交量:",
        volume_ok,
        "MACD:",
        macd_ok
    )

# ==========================
# V5.4 每日交易报告
# ==========================

print()
# ==========================
# V5.4兼容变量
# ==========================

if "fib618_new" not in globals():

    fib618_new = level618

if "fib500_new" not in globals():

    fib500_new = level500

if "fib382_new" not in globals():

    fib382_new = level382
print("================")
print("V5.4 每日报告")
print("================")


report_time = datetime.datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


report = f"""
========================
智能交易日报
========================

时间:
{report_time}


股票:
{name}

代码:
{stock}


当前价格:
{round(price,2)}


技术指标:
----------------

MA5:
{round(float(ma5),2)}

MA10:
{round(float(ma10),2)}

RSI:
{round(rsi_now,2)}

MACD:
{round(macd_now,3)}



波段分析:
----------------

波段低点:
{round(wave_low,2)}

波段高点:
{round(wave_high,2)}


黄金分割:

0.618:
{round(fib618_new,2)}

0.5:
{round(fib500_new,2)}

0.382:
{round(fib382_new,2)}



交易计划:
----------------

观察买入区:

{round(buy_low,2)}
-
{round(buy_high,2)}


确认买点:

{round(confirm_buy,2)}


第一目标:

{round(target1,2)}


第二目标:

{round(target2,2)}


前高目标:

{round(target3,2)}



风险控制:

防守位:

{round(stop_loss,2)}



当前状态:

"""



if price <= fib618_new:

    report += """
🟡 回调区域
等待止跌确认
"""

elif price <= fib500_new:

    report += """
🟢 支撑反弹观察
"""

else:

    report += """
🟠 接近压力区域
"""



report += """

========================
系统结束
========================
"""


filename = (
    name
    + "_交易报告.txt"
)


with open(
    filename,
    "w",
    encoding="utf-8"
) as f:

    f.write(report)



print(report)


print("报告已生成:")
print(filename)


print("================")
print("================")
print(
    "V5.1_full运行完成"
)

print("================")
