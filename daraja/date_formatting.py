from datetime import datetime

def format_date():
    unformatted_current_time = datetime.now()
    formtatted_current_time = unformatted_current_time.strftime('%Y%m%d%H%M%S')

    return formtatted_current_time