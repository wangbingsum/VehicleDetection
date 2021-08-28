import os
import re
import json
from ..model.vehicle import Vehicle

def get_vehicle_data(root_path, models, image_number:dict):
    # 从根目录索引每个车型的图片
    dates = [date for date in os.listdir(
        root_path) if _check_date_formate(date)]
    vehicles = {}
    for date in dates:
        for model in models:
            if model not in vehicles.keys():
                vehicles[model] = []
            path = os.path.join(root_path, date, model)
            if os.path.exists(path):
                number = image_number[model]
                image_path = _get_vehicle_images(path, number)
                vehicles[model].extend(image_path)
    return vehicles

def _get_vehicle_images(root_path, image_number):
    '''
    完整路径形如：D:\Image\20210827\358\Vin\Package\...
    root_path形如: D:\Image\20210827\358
    '''
    # 返回数据列表
    res = []
    vins = [vin for vin in os.listdir(root_path) if _check_vin(vin)]
    for vin in vins:
        # 获取加上vin号后的路径
        vin_path = os.path.join(root_path, vin)
        packages = os.listdir(vin_path)
        for package in packages:
            if _check_package(package):
                # 一辆车图片的完整文件夹
                full_path = os.path.join(vin_path, package)
                images = [f for f in os.listdir(full_path) if _check_file_suffix(f, '.jpg')]
                if images != None and len(images) in image_number:
                    # 生成完整路径下的图片列表
                    full_image_path = _get_full_image_path(full_path, images)
                    vehicle = Vehicle(vin, package, full_image_path)
                    res.append(vehicle)
    return res          

def _get_full_image_path(root_path, iamges):
    '''
    获取完整图片路径列表
    '''
    return [os.path.join(root_path, iamge) for iamge in iamges]     

def _check_file_suffix(filename, suffix):
    '''
    筛选特定后缀的文件
    '''
    return filename.endswith(suffix)

def _check_package(package):
    '''
    检查package格式
    package形如: 4UM167G27OS1
    '''
    pattern = r"^[0-9][A-Z]+.*[A-Z][A-Z0-9]{2}$"
    return len(package) == 12 and re.match(pattern, package) != None
    
def _check_vin(vin):
    '''
    检测vin号格式
    vin形如: LSGUL8AL3MA247727
    '''
    return len(vin) == 17 and vin.startswith('LSG')

def _check_date_formate(date):
    '''
    检查日期格式
    匹配满足yyyyMMdd格式的文件夹
    '''
    return re.match(r'^[0-9]{8}$', date) != None
        