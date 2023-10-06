#!/usr/local/bin/python3.8
# -*- coding: utf-8 -*-
import json
import random
import string
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 检测域名可用性
def check_domain(domain):
    # 执行nslookup {域名}
    try:
        output = subprocess.check_output(f'nslookup {domain} 8.8.4.4', shell=True)
        logging.info(f'output:{output.decode("utf-8")}')
        # 提取出ip address
        ip_address = output.decode('utf-8').rsplit('Address:',1)[1].strip().split('\n')[0]
        logging.info(f'ip_address:{ip_address}')
        # 如果ip address不是ip address，则返回False
        if ip_address== '8.8.4.4' or  not ip_address.replace('.', '').isdigit():
            if not domain.startswith('www'):
                output_ = subprocess.check_output(f'nslookup www.{domain} 8.8.4.4', shell=True)
                ip_address_ = output_.decode('utf-8').rsplit('Address:',1)[1].strip().split('\n')[0]
                if ip_address_== '8.8.4.4' or not ip_address_.replace('.', '').isdigit():
                    return False
                else:
                    return True
            return False
        else:
            return True
    except:
        return False
    
lines = {}
# 读取/root/code/domestic-rules-generator/routing.txt文件
with open('/root/code/domestic-rules-generator/routing.txt', 'r+') as generator_r_f:
    g_lines = generator_r_f.readlines()
    for line in g_lines:
        if line.strip() != '':
            lines[line.strip()] = 0

# 过滤出/datasource/access.log文件中包含[block]的行，并将结果写入到/block.log文件中
def filter_block_to_file():
    # /var/log/xray/
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
        if not check_domain(key):
            logging.info(f'域名:{key}不可用，跳过')
            continue
        if len(key.split('.'))>2:
            new_keys_dict[key.split('.',1)[1]] = 1
            logging.info(f'域名:{key.split(".",1)[1]}可用')
        else:
            new_keys_dict[key] = 1
            logging.info(f'域名:{key}可用')
    
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