import logging as log
import os
import sys
from subprocess import Popen, PIPE
import subprocess
import time
import re
import signal
import warnings
class Check_Box(object):
    "Class check of process, return 1 if person chite on test "
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    warnings.filterwarnings("ignore")
    kol_blacklist = 0
    def __init__(self):
        pass
    def process_check(self):
        "Список всех текущих процессов в системе"
        b = [line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()]
        c = [[b[i].split(' ')[0],re.split(r'\s+',b[i])[1]] for i in range(3,len(b))]
        return c
    def blacklist_check(self):
        "Список запрещенных процессов"
        f = open("blackList.conf", "r")
        l = [line.strip() for line in f]
        f.close()
        return l
    def check(self):
        "Метод проверки процессов из системы с списком запрещенных"
        Check_Box.kol_blacklist=0
        for i in self.blacklist_check():
            for j in self.process_check():
                if j[0]==i:
                    if Check_Box.kol_blacklist == 0:
                        Check_Box.kol_blacklist+=1
                    #print(i)
                    os.kill(int(j[1]),signal.SIGTERM) 
        if Check_Box.kol_blacklist==1:
            return 1
        return 0
c = Check_Box()
while(1):
    c.check()