# ai_waf_v2_sk
AI_WAF_V2是一款利用机器学习开发的针对部分web攻击的安全防御模型，结合了大量的数据学习与开发者的实战经验，总结而成的一套测试框架。

可用作流量旁路监测，提供Server API接口，只需按要求传入字段即可返回判断结果

## 安装方式
```commandline
pip install requirement.txt
```

## 包含模块
- 机器学习检测模块
- libinjection检测模块
- 向量统计模块
- 加权打分模块

## 支持攻击检测
- sql注入识别
- php反序列化识别
- java反序列化识别
- 目录穿越识别
- 系统命令执行识别
- xss跨站攻击识别

## API使用方式
启动api server服务，端口位于9999,入口为svm_waf，携带参数payload
```commandline
python server.py 
```
单条测试，需传入json格式数据如下：
```commandline
http://localhost:9999/svm_waf/?payload={"uri":"http://www.baidu.com/?id=11111' and 1=1 -- "}
```
返回，命中sql注入，命中向量（可忽略）、判断返回概率、libinjection判断结果
```commandline
{"uri": {"attack_type": "sqli", "attack_vec": [1, 0, 1, 0], "probability": [2.400234096532411e-10, 0.9999999997599767], "libinjection": 1}}
```
https://github.com/Stardustsky/ai_waf_v2_sk/blob/main/demo.png

多条测试
```commandline
{"uri":"www.baidu.com/?id=1234","cookie":"PHPSESSION=FUYB274BTRR0876OP"}
```

```commandline
目前支持uri、cookie、body、ua、host、referer、args 七种字段的参数传入
_multi_score_args = dict()
_multi_score_cookie = dict()
_multi_score_body = dict()
_multi_score_referer = dict()
_multi_score_ua = dict()
_multi_score_host = dict()
_multi_score_uri = dict()
```
