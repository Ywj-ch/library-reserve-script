from pathlib import Path
from typing import List, Optional
from datetime import datetime
import re
from ..models.log import LogEntry, LogListResponse, LogStats, LogLevel, LogStatus, LogPagination


class LogService:
    def __init__(self, log_file_path: str = "logs/reserve_seat.log"):
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.is_absolute():
            self.log_file_path = Path(__file__).parent.parent.parent.parent / log_file_path
    
    def parse_log_line(self, line: str) -> Optional[LogEntry]:
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (.+)'
        match = re.match(pattern, line.strip())
        
        if not match:
            return None
        
        timestamp_str, level_str, message = match.groups()
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f').isoformat()
        level = LogLevel(level_str)
        
        seat = None
        status = None
        
        if '预约成功' in message or '成功' in message:
            status = LogStatus.SUCCESS
            seat_match = re.search(r'座位\s+(\w+)', message)
            if seat_match:
                seat = seat_match.group(1)
        elif '预约失败' in message or '失败' in message or '异常' in message:
            status = LogStatus.FAILURE
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            seat=seat,
            status=status
        )
    
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
                log_entry = self.parse_log_line(line)
                if log_entry:
                    all_logs.append(log_entry)
        
        if date_filter:
            all_logs = [log for log in all_logs if date_filter in log.timestamp]
        
        if status_filter:
            all_logs = [log for log in all_logs if log.status and log.status.value == status_filter]
        
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
                log_entry = self.parse_log_line(line)
                if log_entry and log_entry.status:
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
