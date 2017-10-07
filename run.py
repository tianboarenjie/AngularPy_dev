#!/usr/bin/env python3.5
# -*- encoding: utf-8  -*-
"""
@Version: 1.0
@Author: tianbaorenjie
@License: 
@Contact: tianbaorenjie@163.com
@Site: http://
@Software: PyCharm
@Project: AngularPy_dev
@File: run.py
@Time: 10/7/17 11:27 AM
"""
import subprocess
from threading import Thread


def start_django():
    http_host = "192.168.99.250"
    http_port = "8888"
    print("start django")
    subprocess.call("python3.5 ./manage.py runserver %s:%s" % (http_host, http_port), shell=True)


def start_celery():
    print("start celery")
    subprocess.call("python3.5 manage.py celery worker -c 4 --loglevel=info", shell=True)


def main():
    t1 = Thread(target=start_django, args=())
    t2 = Thread(target=start_celery, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
