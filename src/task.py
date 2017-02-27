# coding:utf-8
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI_MYSQL, SQLALCHEMY_POOL_SIZE
from web.www.core.history import History
from web.www.core.weather import Weather
from web.www.core.crawl import Crawl


def init_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE)
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = db_session()
    return session


def run_export_spider_job(current_date=''):
    current = datetime.datetime.now()
    if current_date:
        current = datetime.datetime.strptime(current_date, '%Y-%m')

    crawl_client = Crawl.factory()

    history_spider = 'aqistudy'
    history_client = History.factory()
    history_cities = history_client.get_history_city_all()
    if not history_cities:
        print 'no history city'
        return
    for city in history_cities:
        name = city['city_name']
        history_job = crawl_client.get_crawl_job_info(name, current.year, current.month, history_spider)
        if history_job:
            print 'job existed! city: %s, type, %d' % (name, Crawl.JOB_TYPE_HISTORY, )
            continue
        data = {
            'city_name': name,
            'job_year': current.year,
            'job_month': current.month,
            'job_spider': history_spider,
            'job_type': Crawl.JOB_TYPE_HISTORY,
            'job_status': Crawl.JOB_STATUS_READY,
        }
        if not crawl_client.create_crawl_job_info(data):
            print 'create job failed! city: %s, type, %d' % (name, Crawl.JOB_TYPE_HISTORY, )
        print 'create job success! city: %s, type, %d' % (name, Crawl.JOB_TYPE_HISTORY, )

    weather_spider = 'tianqihoubao'
    weather_client = Weather.factory()
    weather_cities = weather_client.get_weather_city_all()
    if not weather_cities:
        print 'no weather city'
        return
    for city in weather_cities:
        name = city['city_name']
        history_job = crawl_client.get_crawl_job_info(name, current.year, current.month, weather_spider)
        if history_job:
            print 'job existed! city: %s, type, %d' % (name, Crawl.JOB_TYPE_WEATHER, )
            continue
        data = {
            'city_name': name,
            'job_year': current.year,
            'job_month': current.month,
            'job_spider': weather_spider,
            'job_type': Crawl.JOB_TYPE_WEATHER,
            'job_status': Crawl.JOB_STATUS_READY,
        }
        if not crawl_client.create_crawl_job_info(data):
            print 'create job failed: city: %s, type, %d' % (name, Crawl.JOB_TYPE_WEATHER, )
        print 'create job success! city: %s, type, %d' % (name, Crawl.JOB_TYPE_WEATHER, )


def run_crontab():
    # schedule.every(10).minutes.do(run_export_service)
    print 'crontab'

if __name__ == '__main__':
    from web.runhelp import main

    main(__file__, __name__)