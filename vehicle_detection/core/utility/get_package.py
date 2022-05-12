# -*- encoding: utf-8 -*-
'''
@Description: 解析配置文件相关的函数
@Date       :2022/05/12 16:31:44
@Author     :wangbing
@version    :1.0
'''
import json

def get_detial_config(rpo_lst:list, image_number:int, rpo_map:dict) -> dict:
    """ 生成详细配置文件

    Args:
        rpo_lst (list): rpo列表
        image_number (int): 支持的图像张数列表
        rpo_map (dict): rpo和中文名称的映射字典

    Returns:
        dict: 详细的配置信息
    """
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

def generate_and_save_config(config_path:str, target_path:str) -> None:
    """ 生成配置文件并保存

    Args:
        config_path (str): 配置文件路径
        target_path (str): 保存路径
    """
    with open(config_path, 'rb') as f:
        config = json.load(f)
    map = config['rpo_map']
    image_number = config['config']['image_number']
    packages = config['packages']
    with open(target_path, 'w+') as f:
        for key, values in packages.items():
            f.write(f'[{key}]\r')
            rpos = ','.join(values)
            f.write(f'RPO={rpos}\r')
            f.write('Folder=\r')
            pos = get_detial_config(values, image_number, map)
            for key, value in pos.items():
                rpo = ','.join(value)
                f.write(f'{key}={rpo}\r')
            f.write('\r\n')
    print("配置文件生成完成") 