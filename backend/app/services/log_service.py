from pathlib import Path
from typing import List, Optional
from datetime import datetime
import re
import json
from ..models.log import (
    AggregatedLogEntry, LogListResponse, LogStats, 
    LogLevel, LogStatus, LogPagination, SeatAttempt
)


class LogService:
    def __init__(self, log_file_path: str = "logs/reserve_seat.log"):
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.is_absolute():
            self.log_file_path = Path(__file__).parent.parent.parent.parent / log_file_path
    
    def parse_aggregated_log(self, line: str) -> Optional[AggregatedLogEntry]:
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - RESERVE_SESSION: (.+)'
        match = re.match(pattern, line.strip())
        
        if not match:
            return None
        
        timestamp_str, level_str, json_str = match.groups()
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f').isoformat()
        
        try:
            data = json.loads(json_str)
            
            seats = []
            for seat_data in data.get('seats', []):
                seats.append(SeatAttempt(
                    seat_id=seat_data.get('seat_id', ''),
                    status_code=seat_data.get('status_code', 0),
                    response_text=seat_data.get('response_text', ''),
                    success=seat_data.get('success', False)
                ))
            
            status_str = data.get('status', 'pending')
            status = LogStatus.SUCCESS if status_str == 'success' else (
                LogStatus.FAILURE if status_str == 'failure' else LogStatus.PENDING
            )
            
            success_seat = data.get('success_seat')
            total_attempts = data.get('total_attempts', len(seats))
            
            if success_seat:
                message = f"预约成功 - 座位 {success_seat}"
            elif seats:
                failed_seats = ', '.join([s.seat_id for s in seats])
                message = f"预约失败 - 尝试座位: {failed_seats}"
            else:
                message = "无座位尝试记录"
            
            return AggregatedLogEntry(
                session_id=data.get('session_id', ''),
                timestamp=timestamp,
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
                status=status,
                seats=seats,
                details=data.get('details', []),
                success_seat=success_seat,
                total_attempts=total_attempts,
                message=message
            )
        except (json.JSONDecodeError, KeyError) as e:
            return None
    
    def get_logs(
        self,
        page: int = 1,
        limit: int = 20,
        date_filter: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> LogListResponse:
        if not self.log_file_path.exists():
            return LogListResponse(
                logs=[],
                pagination=LogPagination(total=0, page=page, limit=limit)
            )
        
        all_logs = []
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                log_entry = self.parse_aggregated_log(line)
                if log_entry:
                    all_logs.append(log_entry)
        
        if date_filter:
            all_logs = [log for log in all_logs if date_filter in log.timestamp]
        
        if status_filter:
            all_logs = [log for log in all_logs if log.status.value == status_filter]
        
        all_logs.reverse()
        
        total = len(all_logs)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_logs = all_logs[start_idx:end_idx]
        
        return LogListResponse(
            logs=paginated_logs,
            pagination=LogPagination(total=total, page=page, limit=limit)
        )
    
    def get_stats(self) -> LogStats:
        if not self.log_file_path.exists():
            return LogStats(
                total_requests=0,
                success_count=0,
                failure_count=0,
                success_rate=0.0,
                last_success=None
            )
        
        success_count = 0
        failure_count = 0
        last_success = None
        
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                log_entry = self.parse_aggregated_log(line)
                if log_entry:
                    if log_entry.status == LogStatus.SUCCESS:
                        success_count += 1
                        if last_success is None or log_entry.timestamp > last_success:
                            last_success = log_entry.timestamp
                    elif log_entry.status == LogStatus.FAILURE:
                        failure_count += 1
        
        total_requests = success_count + failure_count
        success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0.0
        
        return LogStats(
            total_requests=total_requests,
            success_count=success_count,
            failure_count=failure_count,
            success_rate=round(success_rate, 2),
            last_success=last_success
        )
