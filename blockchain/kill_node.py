#! /bin/python
import os

process_id = os.popen("ps -aux|grep node.py|awk '{print $2}'")
process_id = list(process_id)

for id in process_id[:-1]:
    os.system('kill -9 %s' % id[:-1])

