import logging as log
import os
import sys
from subprocess import Popen, PIPE
import subprocess
import time
import re
import signal
import warnings

class CheckBox(object):
    "Class check of process, return 1 if person chite on test "
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    warnings.filterwarnings("ignore")
    def __init__(self):
        self.kol_blacklist = 0
    def process_check(self):
        "Список всех текущих процессов в системе"
        b = [line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()]
        c = [[b[i].split(' ')[0],re.split(r'\s+',b[i])[1]] for i in range(3,len(b))]
        return c
    def blacklist_check(self):
        "Список запрещенных процессов"
        f = open('blackList.conf', "r")
        l = [line.strip() for line in f]
        f.close()
        return l
    def check(self):
        "Метод проверки процессов из системы с списком запрещенных"
        self.kol_blacklist=0
        for i in self.blacklist_check():
            for j in self.process_check():
                if j[0]==i:
                    if self.kol_blacklist == 0:
                        self.kol_blacklist+=1
                    #print(i)
                    try:
                        os.kill(int(j[1]),signal.SIGTERM)
                    except  PermissionError:
                        return 3
        if self.kol_blacklist==1:
            return 1
        return 0

c = CheckBox()
print(c.check())