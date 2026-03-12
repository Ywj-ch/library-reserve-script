import yaml
import datetime
import urllib3
import logging
import time
import json
import uuid
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

class ReservationSession:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time: Optional[datetime.datetime] = None
        self.end_time: Optional[datetime.datetime] = None
        self.status: str = "pending"
        self.seats: List[Dict[str, Any]] = []
        self.details: List[str] = []
        self.success_seat: Optional[str] = None
    
    def add_detail(self, message: str):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.details.append(f"[{timestamp}] {message}")
    
    def add_seat_attempt(self, seat_id: str, status_code: int, response_text: str, success: bool):
        self.seats.append({
            "seat_id": seat_id,
            "status_code": status_code,
            "response_text": response_text[:200],
            "success": success
        })
        if success and self.status != "success":
            self.status = "success"
            self.success_seat = seat_id

def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_logging():
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=log_dir / "reserve_seat.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='a',
        encoding='utf-8'
    )

def wait_until_send_time(send_time: str, session: ReservationSession):
    hour, minute, second = map(int, send_time.split(':'))
    target_time = datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(hour, minute, second)
    )
    
    session.add_detail(f"等待至 {send_time} 开始发送请求...")
    
    while True:
        now = datetime.datetime.now()
        if now >= target_time:
            session.add_detail(f"到达预约时间 {send_time}，开始执行预约")
            break
        time.sleep(0.5)

def send_reserve_request(config: dict, seat_id: str, session: ReservationSession) -> bool:
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
        session.add_detail(f"正在为座位 {seat_id} 进行预约...")
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        response_text = response.text
        session.add_detail(f"座位 {seat_id} - 状态码: {response.status_code}")
        
        success = False
        try:
            json_response = response.json()
            msg = json_response.get('msg', '')
            session.add_detail(f"座位 {seat_id} - 响应: {msg}")
            if '预约成功' in msg:
                success = True
                session.add_detail(f"座位 {seat_id} 预约成功!")
        except:
            session.add_detail(f"座位 {seat_id} - 响应解析失败")
        
        session.add_seat_attempt(seat_id, response.status_code, response_text, success)
        return success
        
    except Exception as e:
        session.add_detail(f"座位 {seat_id} 请求异常: {e}")
        session.add_seat_attempt(seat_id, 0, str(e), False)
        return False

def log_session(session: ReservationSession):
    session_data = {
        "session_id": session.session_id,
        "start_time": session.start_time.isoformat() if session.start_time else None,
        "end_time": session.end_time.isoformat() if session.end_time else None,
        "status": session.status,
        "seats": session.seats,
        "details": session.details,
        "success_seat": session.success_seat,
        "total_attempts": len(session.seats)
    }
    
    logging.info(f"RESERVE_SESSION: {json.dumps(session_data, ensure_ascii=False)}")

def run_reservation(immediate: bool = False) -> Dict[str, Any]:
    """
    执行预约任务
    
    Args:
        immediate: 是否立即执行（跳过等待时间）
    
    Returns:
        包含执行结果的字典
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    setup_logging()
    
    session = ReservationSession()
    session.start_time = datetime.datetime.now()
    session.add_detail("程序开始执行" + (" (立即执行模式)" if immediate else ""))
    
    try:
        config = load_config()
        session.add_detail("配置加载成功")
        
        if not immediate:
            wait_until_send_time(config['reserve']['send_time'], session)
        else:
            session.add_detail("跳过等待，立即执行预约")
        
        seats = [seat for seat in config['reserve']['seats'] if seat['enabled']]
        max_attempts = min(len(seats), 10)
        
        for i in range(max_attempts):
            seat = seats[i]
            
            success = send_reserve_request(config, seat['id'], session)
            
            if success:
                break
            
            if i < max_attempts - 1:
                delay = config['reserve']['retry']['delay_seconds']
                session.add_detail(f"等待 {delay} 秒后再尝试下一个座位...")
                time.sleep(delay)
        
        session.add_detail("程序执行结束")
        
    except Exception as e:
        session.status = "failure"
        session.add_detail(f"程序执行异常: {e}")
    
    finally:
        session.end_time = datetime.datetime.now()
        if session.status == "pending":
            session.status = "failure"
        log_session(session)
    
    return {
        "session_id": session.session_id,
        "status": session.status,
        "success_seat": session.success_seat,
        "total_attempts": len(session.seats),
        "details": session.details,
        "seats": session.seats
    }

def main():
    run_reservation(immediate=False)

if __name__ == "__main__":
    main()
