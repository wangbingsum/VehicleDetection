import json
from modules.utility.file_process import get_vehicle_data

def test_get_image():
     # 加载配置文件
    with open('config\config.json', 'rb') as fb:
        config = json.load(fb)
    
    root_path = config['image_path']
    models = config['active_model']
    image_number = config['image_number']
    data = get_vehicle_data(root_path, models, image_number)
    for model, vehicle in data.items():
        print(model)
        for v in vehicle:
            print(f' vin: {v.vin}, package: {v.package}')
            for i in range(len(v)):
                position = i + 1
                image = v[position]
                print(f'  {position}: {image}')

if __name__ == '__main__':
    test_get_image()