import json
import os
import sys
import cv2
sys.path.append(r'D:\Project\Python\VehicleDetection')
from modules.utility.file_process import get_vehicle_images


if __name__ == '__main__':
    root_path = r'D:\Image\20210723\358'

    vehicles = get_vehicle_images(root_path, [15])

    with open(r'D:\Project\Python\VehicleDetection\config\UL15.json', 'rb') as f:
        config = json.load(f)

    config_flip = config['flip']

    for vehicle in vehicles:
        print(f'current vechicle: {vehicle.vin}, {vehicle.vehicle_package}')
        for position, image_path in vehicle.items():
            img = cv2.imread(image_path,cv2.IMREAD_COLOR)
            if config_flip[str(position)] == "180":
                # 正常翻转
                # img = cv2.flip(img, flipCode=-1)
                img = cv2.flip(img, flipCode=0)
            # 先判断存图路径是否存在，在进行存图
            save_direction = os.path.join(root_path, "fliped", vehicle.vin, vehicle.vehicle_package)
            if os.path.exists(save_direction) == False:
                os.makedirs(save_direction)
            file_name = os.path.join(save_direction, f'{position}.jpg')
            cv2.imwrite(file_name, img)
            print(f'position{position}: Write successful, path: {file_name}')

