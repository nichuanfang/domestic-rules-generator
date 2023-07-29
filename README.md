# domestic-rules-generator

## 设计初衷

- 由于 xray 客户端使用白名单模式(禁广告,bt 直连,国内域名走直连,其他全部走代理)
- 服务端屏蔽了国内 ip,需要手动在 xray-parser 项目的路由规则手动添加国内域名,比较繁琐
- 配合 github actions 可以实现一劳永逸的在 xray-parser 项目自动添加国内域名路由规则

## 国内域名规则生成器

- 根据 xray 服务端的日志文件 分析出[block]的规则集
- 将规则集去重添加到现有的 xray-parser 项目(client 分支)的路由配置文件中

## 操作步骤

- 从服务器下载/var/log/xray/access.log 文件,放到 datasource 目录下
- 运行 python3 main.py
- 将生成的 routing_body.json 文件拷贝到 xray-parser 项目的 client 分支的 routing 目录下,提交更新
- 客户端更新配置文件
