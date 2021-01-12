# Paper Info Service

论文引文自动爬取项目，给定关键字词，通过百度学术和谷歌学术搜索引擎，爬取最相关的10条论文引文（GB/T7714格式）。

百度学术：requests + 代理池 (原repo地址：https://github.com/jhao104/proxy_pool)

谷歌学术：selenium (FirefoxDrive) + PAC代理


## 代理池启动

**[redis]**
docker run -d -p 6379:6379 \
--name proxy_pool_redis redis \
--requirepass "yourRedisPasswd" 

**[proxy_pool]**
docker run \
-d -p 5010:5010 \
--env DB_CONN=redis://:yourRedisPasswd@IP:6379/redisDBName \
--name proxy_pool \
jhao104/proxy_pool:latest

**注：redisDBName必须为数字**

## 新建配置文件settings.py
```python
SERVER_HOST = 'xxx.xxx.xxx.xxx'
SERVER_PORT = 12345

PROXY_POOL_HOST = 'xxx.xxx.xxx.xxx'
PROXY_POOL_PORT = 12345
```

## API
|API|Method|Description|Arguments|
|:-:|:-:|:-:|:-:|
|/|POST|百度学术|{engine: baidu, keyword: test}|
|/|POST|谷歌学术|{engine: google, keyword: test}|

## Return
[
    "Ando M. IC test equipment: US, US4710704[P]. 1987.",
    "Posada D. Modeltest : testing the model DNA substitution[J]. Bioinformatics, 1998, 14.",
    "Hausman J A. A Specification Test in Econometrics[J]. Econometrica, 1976, 46(185).",
    "Posada D, Crandall K A. modeltest, Ver. 3.06: Testing the Model of DNA Substitution[J]. Bioinformatics, 1998, 14(9):817-818.",
    "Holm S. A simple sequentially rejective multiple test procedure[J]. Scandinavian Journal of Statistics, 1979, 6(2):65-70.",
    "Egger M. Bias in meta-analysis detected by a simple, graphical test[J]. Bmj British Medical Journal, 1997, 316.",
    "Sarah J. Lewis, Stanley Zammit, Gunnell D, et al. Bias in Meta-Analysis Detected by a Simple, Graphical Test[J]. Bmj Clinical Research, 1997, 315(1):629--634.",
    "Smith T O, Drew B T, Toms A P. A meta-analysis of the diagnostic test accuracy of MRA and MRI for the detection of glenoid labral injury[J]. Archives of Orthopaedic & Trauma Surgery, 2012, 132(7):905-919.",
    "White H. A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity[J]. Econometrica, 1980, 48(4):817-838."
]