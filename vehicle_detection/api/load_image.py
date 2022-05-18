# -*- encoding: utf-8 -*-
'''
@Description: 检测数据集图片加载
@Date       :2022/05/17 10:18:35
@Author     :wangbing
@version    :1.0
'''
from ..core.utility import get_vehicle_data


__all__ = ["load_image"]


def load_image(image_root_dir:str, model_name:str, image_number:int) -> list:
    """ 加载单个模型的测试图片

    Args:
        image_root_dir (str): 测试图片根目录
        model_name (str):     模型名称, 例如: 358
        image_number (int):   对应模型检测的图片数目

    Returns:
        list: 加载的测试图片
    """
    
    data = get_vehicle_data(image_root_dir, [model_name], {model_name:[image_number]})
    return data[model_name]
    
    
