#-*- encoding:utf-8 -*-
'''
'''
import re
import types
import platform
import datetime
import os
import time
import signal

from subprocess import PIPE, Popen

class cmd(object):
    def __init__(self, *args, **kwargs):
        self.stdout = None
        self.stderr = None
        self.retcode = None
        self.cmd(*args, **kwargs)
        
    def cmd(self, command, env=None, stdout=PIPE, stderr=PIPE, timeout=None):
            start = datetime.datetime.now()
            ps = None
            if platform.system() == "Linux":
                    ps = Popen(command, stdout=stdout, stderr=stderr, shell=True)
            else:
                    ps = Popen(command, stdout=stdout, stderr=stdout, shell=False)
            while ps.poll() is None:
                    time.sleep(0.2)
                    now = datetime.datetime.now()
                    if (now - start).seconds > timeout:
                            os.kill(ps.pid, signal.SIGINT)
                            self.retcode = -1
                            self.stdout = None
                            self.stderr = None
                            return self

            self.stdout = ps.stdout.readlines()
            self.stderr = ps.stderr.readlines()
            
            if not ps.returncode:
                    self.retcode = ps.returncode

            return self

    def __str__(self):
        import json
        res = {"stdout":self.stdout, "stderr": self.stderr, "retcode": self.retcode}
        return  json.dumps(res, separators=(',', ':'), ensure_ascii=False).encode('utf-8') 
    
    def stdo(self):
        if self.stdout:
            return self.stdout.strip().decode(encoding='UTF-8')
        return ''
    
    def stde(self):
        if self.stderr:
            return self.stderr.strip().decode(encoding='UTF-8')
        return ''
    
    def retcode(self):
        return self.retcode


    def value(self):
        if self.stdout:
            return self.stdout.strip().decode(encoding='UTF-8')
        return ''
