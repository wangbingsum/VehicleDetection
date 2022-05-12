# -*- encoding: utf-8 -*-
'''
@Description: 检测api
@Date       :2022/05/12 16:51:00
@Author     :wangbing
@version    :1.0
'''
import json
import os
from datetime import datetime
from ..core.model import VehicleDetector
from ..core.utility import get_vehicle_data, split_vehicle_data


def model_test(cfg_dir:str, output_dir:str):
    # 读取配置文件
    print('加载配置文件')
    with open(os.path.join(cfg_dir, "config.json"), 'r', encoding="utf-8") as f:
        config = json.load(f)
        
    root_path = config['image_path']
    active_model = config['active_model']
    vehicle_config = config['vehicle_config']
    image_number = config['image_number']
    
    # 预测代码
    print('加载车辆图片')
    data = get_vehicle_data(root_path, active_model, image_number)
    
    for model in active_model:
        model_config = vehicle_config[model]
        number = image_number[model]
        # 获取当前检测模型的检测图片
        vehicle_data = split_vehicle_data(data[model], number)
        
        for key, cfg in model_config.items():
            with open(os.path.join(cfg_dir, cfg), 'r', encoding="utf-8") as f:
                vehicle_cfg = json.load(f)
            detector = VehicleDetector(vehicle_cfg, model, vehicle_data[int(key)])
            result = detector.run()
            if result is not None:
                # 对检测结果进行后处理
                process_detection_result(model, result, vehicle_cfg['config'], output_dir) 

def process_detection_result(model:str, result, config:dict, output_dir:str):
    date = datetime.now()
    date_dir = date.strftime('%Y%m%d')

    path = os.path.join(output_dir, date_dir, model)
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存检测结果
    image_number = config["image_number"]
    file_name = os.path.join(path, f'DetectionResults_{image_number}.csv')
    vehicle_high_name = os.path.join(path, f'DetectionResults_{image_number}_high.csv')
    vehicle_low_name = os.path.join(path, f'DetectionResults_{image_number}_low.csv')
    vehicle_high, vehicle_low = split_vehicle_detection_result(result, config)
    save_csv(file_name, result)
    save_csv(vehicle_high_name, vehicle_high)
    save_csv(vehicle_low_name, vehicle_low)
    print(f'model: {model}, 检测结果写入成功: ')
    print("\tpath:{file_name}")
    print("\vehicle high:{vehicle_high_name}")
    print("\vehicle low:{vehicle_low_name}")

def split_vehicle_detection_result(detection_result, config):
    high = config['high'] # 32/33/42/45/B5/B7
    vehicle_high = []
    vehicle_low = []
    for vehicle in detection_result:
        package = vehicle[1][7:7+2]
        if package in high:
            vehicle_high.append(vehicle)
        else:
            vehicle_low.append(vehicle)
    return vehicle_high, vehicle_low

def save_csv(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as writer:
        for vehicle in data:
            write_data = ','.join(vehicle)
            writer.write(write_data)
            writer.write('\n')
