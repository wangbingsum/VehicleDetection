# -*- encoding: utf-8 -*-
'''
@Description: 文件处理,车辆图片加载
@Date       :2022/05/12 16:05:24
@Author     :wangbing
@version    :1.0
'''
import os
import re
from ..model.vehicle import Vehicle

def split_vehicle_data(data:dict, image_number:list) ->dict:
    """ 对给定模型的检测图片进行拆分"""
    res = {}
    for num in image_number:
        res[num] = []
    for vehicle in data:
        res[len(vehicle)].append(vehicle)
            
    return res

def get_vehicle_data(root_path:str, models:list, image_number:dict) -> dict:
    """从给定目录搜索所有检测图片

    Args:
        root_path (str): 搜索图片的根目录
        models (list): 模型名称列表
        image_number (dict): 一个车型配置下支持的图片检测张数

    Returns:
        dict: 检测图片数据
    """
    # 解析第一层日期目录
    dates = [date for date in os.listdir(root_path) 
            if _check_date_formate(date)]
    
    vehicles = {}
    for date in dates:
        for model in models:
            if model not in vehicles.keys():
                vehicles[model] = []
            path = os.path.join(root_path, date, model)
            if os.path.exists(path):
                number_lst = image_number[model]
                image_path = _get_vehicle_images(path, number_lst)
                # 以展开为列表的形式进行添加
                vehicles[model].extend(image_path)
    return vehicles

def get_header(root_path:str) -> list:
    """_summary_

    Args:
        root_path (str): 搜索目录

    Returns:
        list: 所有符合日期格式的子目录列表
    """
    dates = [date for date in os.listdir(root_path) if _check_date_formate(date)]
    return dates

def _get_vehicle_images(root_path:str, image_number:list) -> list:
    """ 
        完整路径形如: D:\Image\20210827\358\{Vin}\{Package}\...
        
        root_path形如: D:\Image\20210827\358

    Args:
        root_path (str): 搜索根目录在vin号层级
        image_number (list): 符合要求的图片张数的列表

    Returns:
        list: 搜索到的图片列表
    """
    # 返回数据列表
    res = []
    vins = [vin for vin in os.listdir(root_path) 
            if _check_vin(vin)]
    
    for vin in vins:
        # 获取加上vin号后的路径
        vin_path = os.path.join(root_path, vin)
        packages = [package for package in os.listdir(vin_path) 
                    if _check_package(package)]
        
        for package in packages:
            # 一辆车图片的完整文件夹
            full_path = os.path.join(vin_path, package)
            images = [image for image in os.listdir(full_path) 
                    if _check_file_suffix(image, '.jpg')]
            
            if images != None and len(images) in image_number:
                # 生成完整路径下的图片列表
                full_image_path = _get_full_image_path(full_path, images)
                vehicle = Vehicle(vin, package, full_image_path)
                res.append(vehicle)
    return res          

def _get_full_image_path(root_path:str, images:list) -> list:
    """ 获取完整图片路径列表

    Args:
        root_path (str): 图片根目录
        images (list): 图片相对路径

    Returns:
        list: 合成的绝对路径列表
    """
    return [os.path.join(root_path, image) for image in images]     

def _check_file_suffix(filename, suffix):
    '''
    筛选特定后缀的文件
    '''
    return filename.endswith(suffix)

def _check_package(package:str) -> bool:
    """ 检查package格式,package形如: 4UM167G27OS1或者4UM167G27

    Args:
        package (str): package字符

    Returns:
        bool: 检测结果
    """
    if len(package) == 12:
        pattern = r"^[0-9A-Z]+.*[A-Z][A-Z0-9]{2}$"
        return re.match(pattern, package) != None
    
    elif len(package) == 9:
        pattern = r"^[0-9A-Z]{9}$"
        return re.match(pattern, package) != None
    
    else:
        return False 
    
def _check_vin(vin:str) -> bool:
    """ 检查vin号格式,vin形如: LSGUL8AL3MA247727

    Args:
        vin (str): vin号字符

    Returns:
        bool: 检测结果
    """
    return len(vin) == 17 and vin.startswith('LSG')

def _check_date_formate(date:str) -> bool:
    """ 检查日期格式,匹配满足yyyyMMdd格式的文件夹

    Args:
        date (str): 日期字符串

    Returns:
        bool: 匹配结果
    """
    return re.match(r'^[0-9]{8}$', date) != None
        