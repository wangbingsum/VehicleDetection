#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:配置文件生成脚本
@Date       :2021/09/03 21:32:59
@Author     :wangbing
@version    :1.0
'''
import json

def get_detial_config(rpo_lst:list, image_number, rpo_map:dict):
        "生成详细配置文件"
        map = {}
        for rpo in rpo_lst:
            map[rpo] = rpo_map[rpo]
        # 初始化拍摄点位和rpo映射字典
        pos = {}
        for i in range(1, image_number + 1):
            pos[i] = []
        # 迭代获取拍摄点位对应rpo
        for key, values in map.items():
            for value in values:
                pos[value].append(key)
                    
        return pos

if __name__ == '__main__':
    with open('config/NB.json', 'rb') as f:
        config = json.load(f)
    map = config['rpo_map']
    filename = 'output/result.txt'
    packages = config['packages']
    with open(filename, 'w+') as f:
        for key, values in packages.items():
            f.write(f'[{key}]\r')
            rpos = ','.join(values)
            f.write(f'RPO={rpos}\r')
            f.write('Folder=\r')
            pos = get_detial_config(packages['6NB268T01'], 14, map)
            for key, value in pos.items():
                rpo = ','.join(value)
                f.write(f'{key}={rpo}\r')
            f.write('\r\n')
     