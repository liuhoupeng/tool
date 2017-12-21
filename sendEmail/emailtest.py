#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import logging
import smtplib
import socket 
import signal
import ConfigParser
from datetime import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


CONF_PATH = "/etc/zabbix/alarm_email.conf"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    filename='/var/log/zabbix/send_alarm_email.log')

class EmailObject:

    def __init__(self,to_addr,content):
        self.timeout = 10
        self.retry = 3
        self.cp = self._parse_config()
        self.cpl = self._parse_config().sections()
        self.conf = dict(self.cp.items(self.cpl[0])) 
        # common how to use one
        self.to_addr = to_addr
        self.content = content

    # get ConfigParser,for section selection
    def _parse_config(self):
        cp = ConfigParser.ConfigParser()
        cp.read(CONF_PATH)
        return cp

    # set base config
    def _conf_parse(self):
        self.subject = "zabbix告警"
        self.from_addr = self.conf["from_addr"]
        self.password = self.conf["password"]
        self.smtp_server = self.conf["smtp_server"]

    def _msg_parse(self):
        #msg = self.content.split("*")
        #state = "alarm" if msg[0] == "PROBLEM" else "ok"
        #severity = msg[1]
        #head_time = map(int,msg[2].split("."))
        #tail_time = map(int,msg[3].split(":"))
        ## if not host?
        #event_type = "host." + msg[4]
        #reason = msg[5].replace("_"," ")
        #alarm_id = int(msg[6])
        #message = msg
        return self.content

    def _change_server(self):
        # if len = 1 and this fun is called,means that all servers hava been tried
        if(len(self.cpl) > 1):
            self.cpl.pop(0)
            self.retry = 3
            self.conf = dict(self.cp.items(self.cpl[0]))
            logging.info("Change server to {}".format(self.cpl[0]))
            self.send_email()
        else:
            logging.warning("No server could be used,try to config more server(now is {}) or increase the timeout [{}]!".format(self.cp.sections(),self.timeout))
            exit()
  
    def send_email(self):
        # signal handle   
        def handler(signum,frame):
            if self.retry > 0:
                raise AssertionError
            else:
                self._change_server()

        self._conf_parse()
        from_addr = self.from_addr 
        password = self.password
        smtp_server = self.smtp_server
        timeout = self.timeout
        to_addr = self.to_addr

        msg = MIMEText(self.content,'plain','utf-8')
        msg['Subject'] = Header(self.subject, 'utf-8')
        msg['From'] = 'AlarmEmail'+'<'+from_addr+'>'    
        msg['To'] = "hpliu5898@fiberhome.com"
        
        try:
            signal.signal(signal.SIGALRM,handler)
            signal.alarm(timeout)
            server = smtplib.SMTP_SSL(smtp_server,465)
            server.login(from_addr, password)
            server.sendmail(from_addr,to_addr, msg.as_string())
            logging.info("Send email successfully!From:[{}],To:[{}],Content:[{}]".format(from_addr,to_addr,self.content))
            server.quit()
            exit()
        except AssertionError:
            self.retry -= 1
            logging.info("Begin to resend email for the {}th times".format(3-self.retry))
            self.send_email()
        except smtplib.SMTPAuthenticationError,e:
            logging.error("Server [{}] authentication failed".format(smtp_server))
            self._change_server()

'''
example:

from emailtest import emailtest


eb = emailtest.EmailObject("hpliu5898@fiberhome.com","test content")
eb.send_email()

tips:
increase timeout:
    eb.timeout = 10
increase retry times:
    eb.retry = 5
'''

