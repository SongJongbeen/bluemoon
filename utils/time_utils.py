from datetime import datetime
import pytz

KST = pytz.timezone('Asia/Seoul')

def is_target_time(target_hour: int, target_minute: int) -> bool:
    now = datetime.now(KST)
    return now.hour == target_hour and now.minute == target_minute

def is_every_hour(minute=0):
    now = datetime.now(KST)
    return now.minute == minute

def is_every_half_hour(minutes=[0, 30]):
    now = datetime.now(KST)
    return now.minute in minutes

def is_specific_hours(hours, minute=0):
    now = datetime.now(KST)
    return now.hour in hours and now.minute == minute

def is_operation_hours() -> bool:
    now = datetime.now(KST)
    # 1시부터 8시까지는 False 반환
    return not (1 <= now.hour < 8)
