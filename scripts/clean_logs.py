"""
日志清理脚本 - 保留最近30天的日志
"""
from datetime import datetime, timedelta
from pathlib import Path

def clean_old_logs(log_file: str = "logs/reserve_seat.log", keep_days: int = 30):
    """
    清理旧日志，保留最近N天的日志
    
    Args:
        log_file: 日志文件路径
        keep_days: 保留的天数
    """
    log_path = Path(__file__).parent.parent / log_file
    
    if not log_path.exists():
        print(f"日志文件不存在: {log_path}")
        return
    
    # 读取所有日志
    with open(log_path, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    if not all_lines:
        print("日志文件为空")
        return
    
    # 计算截止日期
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    
    print(f"清理日志: 保留 {keep_days} 天内的日志")
    print(f"截止日期: {cutoff_str}")
    
    # 过滤日志
    kept_lines = []
    removed_count = 0
    
    for line in all_lines:
        # 提取日期 (格式: 2025-01-04 07:00:03)
        if line and len(line) >= 10:
            date_str = line[:10]
            try:
                log_date = datetime.strptime(date_str, '%Y-%m-%d')
                if log_date >= cutoff_date:
                    kept_lines.append(line)
                else:
                    removed_count += 1
            except:
                # 如果无法解析日期，保留该行
                kept_lines.append(line)
    
    # 写回文件
    with open(log_path, 'w', encoding='utf-8') as f:
        f.writelines(kept_lines)
    
    print(f"\n清理完成:")
    print(f"  原始行数: {len(all_lines)}")
    print(f"  保留行数: {len(kept_lines)}")
    print(f"  删除行数: {removed_count}")

if __name__ == "__main__":
    clean_old_logs(keep_days=30)
