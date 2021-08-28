import json
import os
from datetime import datetime
import pandas as pd
from modules.model.detection import VehilceDetection
from modules.utility.file_process import get_vehicle_data

def main():
    print('加载配置文件')
    with open('./config/config.json', 'rb') as f:
        config = json.load(f)
    root_path = config['image_path']
    active_model = config['active_model']
    vehicle_config = config['vehicle_config']
    image_number = config['image_number']
    print('加载车辆图片')
    data = get_vehicle_data(root_path, active_model, image_number)
    for model in active_model:
        vehicle_config_file = vehicle_config[model]
        for cfg in vehicle_config_file:
            with open(os.path.join('config', cfg), 'rb') as f:
                vehicle_config = json.load(f)
            detector = VehilceDetection(vehicle_config, model, data[model])
            result = detector.run()
            save_detection_result(model, result)

def save_detection_result(model, result):
    root_path = 'output'
    date = datetime.now()
    date_dir = date.strftime('%Y%m%d')
    path = os.path.join(root_path, date_dir, model)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = os.path.join(path, 'DetectionResults.csv')
    with open(file_name, 'w') as writer:
        for vehicle in result:
            write_data = ','.join(vehicle)
            writer.write(write_data)
            writer.write('\n')
    print(f'model: {model}, 检测结果写入成功, path: {file_name}')


if __name__ == '__main__':
    # main()
    with open('./config/UL15.json', 'rb') as f:
        config = json.load(f)
    print(config)
    