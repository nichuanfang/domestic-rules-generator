# domestic-rules-generator

## 设计初衷
* 由于xray客户端使用白名单模式(禁广告,bt直连,国内域名走直连,其他全部走代理)
* 服务端屏蔽了国内ip,需要手动在xray-parser项目的路由规则手动添加国内域名,比较繁琐
* 配合github actions可以实现一劳永逸的在xray-parser项目自动添加国内域名路由规则

## 国内域名规则生成器
* 根据xray服务端的日志文件 分析出[block]的规则集
* 将规则集去重添加到现有的xray-parser项目(client分支)的路由配置文件中
