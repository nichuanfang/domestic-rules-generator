#!/bin/bash

cd /root/code/domestic-rules-generator && git pull
cd /root/code/xray-parser && git checkout client && git pull
python3.8 /root/code/domestic-rules-generator/main.py
git config --global user.email "f18326186224@gmail.com"
git config --global user.name "jayncfzzz"
cd /root/code/xray-parser && git add . && git commit -m "更新客户端block规则" && git push
cd /root/code/domestic-rules-generator && git add . && git commit -m "更新增量文件" && git push
