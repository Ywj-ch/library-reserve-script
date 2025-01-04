import requests
import datetime
import urllib3
import logging
import time
import random

# 设置日志记录
logging.basicConfig(
    filename="D:/Develop/Python/python_test1/reserve_seat.log",  # 设置日志文件路径
    level=logging.INFO,  # 日志等级
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
    filemode='a',  # 追加写入模式
    encoding='utf-8'  # 设置编码格式为utf-8
)

# URL 地址
url = "https://libwx.hunnu.edu.cn/apim/seat/SeatDateHandler.ashx"

# 请求头，从 Raw 中提取
headers = {
    "Host": "libwx.hunnu.edu.cn",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090c11) XWEB/11529 Flue",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://libwx.hunnu.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://libwx.hunnu.edu.cn/mobile/html/seat/seatquickbook.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "ASP.NET_SessionId=lsmlbmz3o1is0wen2pd2a20e; cookie_unit_name=%e6%b9%96%e5%8d%97%e5%b8%88%e8%8c%83%e5%a4%a7%e5%ad%a6%e5%9b%be%e4%b9%a6%e9%a6%84; cookie_come_app=D935AE54952F16C1; cookie_come_timestamp=1735883621; cookie_come_sno=DAD084FF07CB0C559615A8774898B543BDD91BDADE4A1FCA; dt_cookie_user_name_remember=3A76B31CCB4E607689DB161097F0C475B33A1172D44AE9EB"
}

# 表单数据模板
data_template = {
    "code": "AF2D2FCC651B0748EE657B92EC48C8994285D1F738DE26D96FC687FEB56E919716CB6805F9903F6BFEF2B13F07A0373772D52AEEE21A7C704C9CE1999A544AC2",
    "data_type": "seatDate",
    "seatdate": "today",
    "datetime": "780,1350"
}

# 需要预约的座位列表
seat_list = ["Z41N006", "Z41N005", "Z41N259"]

# 忽略警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 开始记录日志
logging.info("程序开始执行")

# 随机打乱座位顺序
random.shuffle(seat_list)

# 定义尝试次数
attempts = 3

for i in range(attempts):
    seat = seat_list[i]  # 从随机顺序中选择座位

    # 更新表单数据中的座位号
    data = data_template.copy()
    data["seatno"] = seat
    data["seatname"] = seat[-3:]  # 从座位号的最后三位获取座位名称

    try:
        # 发送 POST 请求
        logging.info(f"正在为座位 {seat} 进行预约...")
        logging.info(f"正在进行第 {i + 1} 次请求...")

        logging.info("发送预约请求...")
        response = requests.post(url, headers=headers, data=data, verify=False)

        # 记录响应信息
        logging.info(f"状态码: {response.status_code}")
        logging.info(f"响应内容: {response.text}")

        # 打印当前时间到日志
        current_time = datetime.datetime.now()
        logging.info(f"任务执行时间：{current_time}")

        # 如果需要间隔时间
        if i < attempts - 1:
            logging.info(f"等待 2 秒后再尝试下一次请求...")
            time.sleep(2)

    except Exception as e:
        # 捕获异常并记录
        logging.error(f"程序执行时发生异常: {e}")

# 结束记录日志
logging.info("程序执行结束")
