# sendEmail

## step
### 1.install
```
pip install emailtest-1.0.tar.gz
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