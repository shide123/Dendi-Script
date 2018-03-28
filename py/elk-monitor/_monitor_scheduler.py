# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from pip.utils import logging
import monitor

# apscheduler 介绍：
# BlockingScheduler：仅可用在当前你的进程之内，与当前的进行共享计算资源
# BackgroundScheduler:　在后台运行调度，不影响当前的系统计算运行
# AsyncIOScheduler:　如果当前系统中使用了async module，则需要使用异步的调度器
# GeventScheduler:　如果使用了gevent，则需要使用该调度
# TornadoScheduler:　如果使用了Tornado, 则使用当前的调度器
# TwistedScheduler:Twister应用的调度器
# QtScheduler:　Qt的调度器


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(monitor.mysql_monitor, 'interval', seconds=900)
    scheduler.add_job(monitor.nginx_monitor, 'interval', seconds=900)
    scheduler.start()
