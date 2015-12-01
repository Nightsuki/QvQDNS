#QvQDNS
一个基于Tornado、Peewee用于记录 DNS 和 HTTP 请求的工具

### Fetures
* DNS 记录
* HTTP 记录

### Demo
* [Demo Link](http://www.qvq.io)

### Running
```
qvqdns.py - DNS服务(记录DNS请求)

qvqweb.py - HTTP服务(记录HTTP请求)

main.py - 控制面板
```

用 ```gunicorn```  启动控制面板 ```gunicorn main:application -c gunicorn.py```

### License
MPL