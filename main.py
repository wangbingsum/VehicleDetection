import json
import os
import sys
from datetime import datetime
import pandas as pd
from modules.model.detection import VehilceDetector
from modules.utility.file_process import get_vehicle_data

DIRNAME = ''


def main():
    # 读取配置文件
    print('加载配置文件')
    with open('./config/config.json', 'rb') as f:
        config = json.load(f)
    root_path = config['image_path']
    active_model = config['active_model']
    vehicle_config = config['vehicle_config']
    image_number = config['image_number']
    
    # 预测代码
    print('加载车辆图片')
    data = get_vehicle_data(root_path, active_model, image_number)
    for model in active_model:
        vehicle_config_file = vehicle_config[model]
        vehicle_data = split_vehicle_data(data[model])
        for key, cfg in vehicle_config_file.items():
            with open(os.path.join('config', cfg), 'rb') as f:
                vehicle_cfg = json.load(f)
            detector = VehilceDetector(vehicle_cfg, model, vehicle_data[int(key)])
            result = detector.run()
            # 对检测结果进行处理
            process_detection_result(model, result, vehicle_cfg['config'])

def split_vehicle_data(data, image_number):
    res = {}
    for num in image_number:
        res[num] = []
    for vehicle in data:
        res[len(vehicle)].append(vehicle)
    return res

def process_detection_result(model, result, config):
    root_path = 'output'
    date = datetime.now()
    date_dir = date.strftime('%Y%m%d')

    path = os.path.join(root_path, date_dir, model)
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存检测结果
    image_number = config["image_number"]
    file_name = os.path.join(path, f'DetectionResults_{image_number}.csv')
    vehicle_high_name = os.path.join(path, 'DetectionResults_{image_number}_high.csv')
    vehicle_low_name = os.path.join(path, 'DetectionResults_{image_number}_low.csv')
    vehicle_high, vehicle_low = split_vehicle_detection_result(result, config)
    save_csv(file_name, result)
    save_csv(vehicle_high_name, vehicle_high)
    save_csv(vehicle_low_name, vehicle_low)
    full_path = os.path.join(DIRNAME, file_name)
    print(f'model: {model}, 检测结果写入成功, path: {full_path}, \
        vehicle high: {os.path.join(DIRNAME, vehicle_high_name)} \
        vehicle low: {os.path.join(DIRNAME, vehicle_low_name)}')

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

if __name__ == '__main__':
    DIRNAME, _ = os.path.split(os.path.abspath(sys.argv[0]))
    # main()
    