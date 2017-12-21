# sendEmail

## step
### 1.install
```
pip install emailtest-1.0.tar.gz
<<<<<<< HEAD

mkdir /etc/zabbix
cp alarm_email.conf /etc/zabbix
=======
>>>>>>> 30db7cfb1966070782c5513f00dd608b62c3f072
```
### 2.example
```
from emailtest import emailtest


eb = emailtest.EmailObject("hpliu5898@fiberhome.com","test content")
eb.send_email()

#tips:
#increase timeout:
#    eb.timeout = 10
#increase retry times:
#    eb.retry = 5
```