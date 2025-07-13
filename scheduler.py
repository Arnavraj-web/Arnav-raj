from apscheduler.schedulers.background import BackgroundScheduler
from price_tracker import check_prices

def start_scheduler(bot):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: check_prices(bot), 'interval', hours=1)
    scheduler.start()
