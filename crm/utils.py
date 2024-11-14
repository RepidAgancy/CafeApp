def calculate_percentage_change(today_value, yesterday_value):
    if yesterday_value == 0:
        return 0
    return round(((today_value - yesterday_value) / yesterday_value) * 100, 2)
