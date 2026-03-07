import yaml
import datetime
import urllib3
import logging
import time
import requests
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_logging():
    """配置日志系统"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=log_dir / "reserve_seat.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='a',
        encoding='utf-8'
    )

def wait_until_send_time(send_time: str):
    """等待到发送时间"""
    hour, minute, second = map(int, send_time.split(':'))
    target_time = datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(hour, minute, second)
    )
    
    logging.info(f"等待至 {send_time} 开始发送请求...")
    
    while True:
        now = datetime.datetime.now()
        if now >= target_time:
            logging.info(f"到达预约时间 {send_time}，开始执行预约")
            break
        time.sleep(0.5)

def send_reserve_request(config: dict, seat_id: str):
    """发送预约请求"""
    url = config['request']['url']
    
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
        "Cookie": config['auth']['cookie']
    }
    
    data = {
        "code": config['auth']['code'],
        "data_type": config['request']['data_template']['data_type'],
        "seatdate": config['request']['data_template']['seatdate'],
        "datetime": config['request']['data_template']['datetime'],
        "seatno": seat_id,
        "seatname": seat_id[-3:]
    }
    
    try:
        logging.info(f"正在为座位 {seat_id} 进行预约...")
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        logging.info(f"状态码: {response.status_code}")
        logging.info(f"响应内容: {response.text}")
        
        return response
    except Exception as e:
        logging.error(f"预约请求失败: {e}")
        raise

def main():
    """主函数"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    setup_logging()
    logging.info("程序开始执行")
    
    try:
        config = load_config()
        logging.info("配置加载成功")
        
        wait_until_send_time(config['reserve']['send_time'])
        
        seats = [seat for seat in config['reserve']['seats'] if seat['enabled']]
        max_attempts = min(len(seats), config['reserve']['retry']['max_attempts'])
        
        for i in range(max_attempts):
            seat = seats[i]
            
            try:
                send_reserve_request(config, seat['id'])
                
                current_time = datetime.datetime.now()
                logging.info(f"任务执行时间：{current_time}")
                
                if i < max_attempts - 1:
                    delay = config['reserve']['retry']['delay_seconds']
                    logging.info(f"等待 {delay} 秒后再尝试下一次请求...")
                    time.sleep(delay)
            
            except Exception as e:
                logging.error(f"第 {i + 1} 次预约失败: {e}")
        
        logging.info("程序执行结束")
    
    except Exception as e:
        logging.error(f"程序执行异常: {e}", exc_info=True)

if __name__ == "__main__":
    main()
