### 简介
一个简易的HTTP代理列表更新API，基于Flask  
### 安装依赖 
pip install -r require.txt
### 模块
getProxyIP.py　　更新可用代理IP列表  
getProxyAPI.py　　API接口，显示可用IP列表，并提供更新列表接口，默认接口地址：127.0.0.1:9999/  
updateip.py　　更新从各站点爬取的代理IP列表（未测试可用性），可通过手动添加系统定时任务刷新IP列表  
proxy.json　　代理IP列表（未检测）文件，getProxyIP.py读取此文件刷新可用代理IP列表  
proxyvivdip.json  可用代理IP列表，通过getProxyAPI.py接口请求产生并读取  
### 自定义配置
1. 修改API监听地址：  
```python
getProxyAPI.py :

app.run(host='127.0.0.1', port=9999, threaded=True)
# host：监听地址    port： 监听端口
```
2. 修改刷新可用代理IP列表时的线程数：  
```python
getProxyIP.py :

MAX_THREAD = 2000
```
3. 修改刷新重置时间：
```python
getProxyAPI.py

UPDATETIME = 180
```
