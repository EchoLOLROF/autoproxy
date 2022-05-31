# AUTOPROXY
autoproxy可读取docker container的environment变量，自动生成nginx的反向代理配置。

# 使用方法
```yaml
version: '2'

services:
  whoami:
    image: jwilder/whoami
    ports:
     - 1234:8000
    environment:
      - VIRTUAL_PORT=1234
      - VIRTUAL_PATH=^~/whoami/
```
```bash
docker-compose up -d
python generate_conf.py > /nginx-config-path/nginx.conf
service nginx reload
```

```bash
curl localhost/whoami/
I'm ab0297418e72
```

autoproxy提供了默认的模板[default.template](default.template)

environment需要配置
- VIRTUAL_PORT 为需要反向代理的服务的端口号
- VIRTUAL_PATH 为需要配置的二级目录路径
- VIRTUAL_DEST 默认为 '/'，可根据需要修改

# 扩展
如果需要自定义模板，则新增template后缀的文件，template使用python string中的[Template语法](https://docs.python.org/3/library/string.html#template-strings)

例如新增test.template
```template
location ${PATH} {
    include proxy.conf;
    rewrite ${REWRITE} break;
    proxy_pass http://localhost:${PORT}${DEST};
}
```
在docker container的environment中配置`VIRTUAL_TEMPLATE=test`，因上述模板需要`${REWRITE}`变量，则需要在environment中配置`VIRTUAL_REWRITE`

执行`python generate_conf.py > /nginx-config-path/nginx.conf`即可生成新的配置

# Thanks
[nginx-proxy](https://github.com/nginx-proxy/nginx-proxy)
