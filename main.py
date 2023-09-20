#!/usr/local/bin/python3.8
# -*- coding: utf-8 -*-
import json
import random
import string

lines = {}
# 读取/root/code/domestic-rules-generator/routing.txt文件
with open('/root/code/domestic-rules-generator/routing.txt', 'r+') as generator_r_f:
    g_lines = generator_r_f.readlines()
    for line in g_lines:
        if line.strip() != '':
            lines[line.strip()] = 0

# 过滤出/datasource/access.log文件中包含[block]的行，并将结果写入到/block.log文件中
def filter_block_to_file():
    with open('/var/log/xray/access.log', 'r+') as f:
            for line in f:
                if '[block]' in line:
                    # 获取accepted和[block]之间的域名
                    domain = line.split('accepted')[1].split('[block]')[0].strip().split(':')[1]
                    # 如果domain不是ip address
                    if not domain.replace('.', '').isdigit():
                        if domain.strip() != '':
                            lines[domain] =  0
    
    # 对keys处理
    new_keys_dict = {}
    for key in lines.keys():
        if len(key.split('.'))>2:
            new_keys_dict[key.split('.',1)[1]] = 1     
            
    # 将res_dist的keys写入routing_body.json的rules中
    with open('/root/code/domestic-rules-generator/routing_template_body.json', 'r+') as f:
        str_json = json.loads(f.read())
        
        for new_key in new_keys_dict.keys():
            # {
            #     "id": "qO1yH8rK5nG6qQ0f",
            #     "type": "field",
            #     "outboundTag": "direct",
            #     "domain": [
            #         "codemart.com"
            #     ]
            # }
            # 生成16位随机字符串
            id = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            str_json['rules'].append({
                'id': id,
                'type': 'field',
                'outboundTag': 'direct',
                'domain': [new_key]
            })
        # 将res_dict的keys写入routing.txt文件中 增量更新需要用到
        with open('/root/code/domestic-rules-generator/routing.txt', 'w+') as f:
            for new_key in new_keys_dict.keys():
                f.write(new_key + '\n')
                
        # 将str_json写入到dist/routing_body.json文件中
        with open('/root/code/xray-parser/routing/routing_body.json', 'w+') as f:
            f.write(json.dumps(str_json, indent=4))
            
                    
if __name__ == '__main__':
    filter_block_to_file()                    