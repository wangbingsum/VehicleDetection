import numpy as np
import json
import os
import re
# from ..predict.UL.predict import model

class VehilceDetection:
    def __init__(self, config:dict, model, vehicles:list):
        super().__init__()
        self.map = config['rpo_map'] # rpo到拍摄位置的映射
        self.packages = config['packages'] # 车型配置
        self.class2rpo = config['class_to_rpo'] # 英文类别到rpo的映射
        self.rpo2description = config['rpo_to_description'] # rpo到中文的映射
        self.componets = config['componets']
        self.config = config['config']
        self.model = model # 当前检测的模型
        self.vehicles = vehicles # 检测车辆信息列表

    def run(self):
        print(f'当前检测车型：{self.model}')
        print("模型初始化")
        model_path = self.config['model_path']
        self._init_model(model_path)
        detection_results = []
        # 检测当前车型下的所有车辆图片
        total_vehicle = len(self.vehicles)
        for index, vehicle in enumerate(self.vehicles):
            print(f'{index}/{total_vehicle} vin: {vehicle.vin}, package: {vehicle.vehicle_package}')
            # 轮询检测每一张图片
            rpos = self.packages[vehicle.package]
            # 获取当前配置下每个拍摄位置对应的rpo列表
            pos_config = self.get_detial_config(rpos)
            result = []
            result.append(vehicle.vin)
            result.append(vehicle.vehicle_package)
            for i in range(1, len(vehicle) + 1):
                result.append(f'PIC{i}')
                camera_id = min(i, 6)
                image_path = vehicle[i]
                componet = self.componets[str(i)]
                # 构造调用json文件
                image_json = self.get_image_json(image_path, componet, camera_id, self.model)
                # 调用模型
                result_json = self.predict(image_json)
                # 解码得到当前拍摄位置的预测类别信息
                predict_cls = self.decode(componet, result_json)
                # 对比配置文件和预测信息，获取检测结果
                res = self.compare(i, pos_config[i], predict_cls)
                if res != 'OK':
                    result.extend(['NG', res])
                else:
                    result.extend(['OK', ' '])
            # 插入一辆车总的检测结果
            if 'NG' in result:
                result.insert(2, 'NG')
            else:
                result.insert(2, 'OK')
            detection_results.append(result)
        return detection_results

    def compare(self, position, acutal:list, predict:list):
        '''
        比对预测类别和实际类别，得到预测结果
        1. 预测少了
        2. 预测错了
        '''
        pre = ' '.join(predict)
        acu = ' '.join(acutal)
        if len(predict) != len(acutal):
            return f'position: {position} 预测类别个数不等于实际个数：acutal: {acu} predict: {pre}'
        elif not self._check_element_equal(predict, acutal):
            return f'position: {position} 预测类别不完全等于实际类别: acutal: {acu} predict: {pre}'
        else:
            return 'OK'
            
    def _check_element_equal(self, predict, actual):
        for pre in predict:
            if pre not in actual: return False
        return True

    def decode(self, componet, result_json): 
        '''
        返回当前拍摄位置，预测到的所有类别信息
        '''
        res = []
        for comp in componet:
            img_cls = result_json['result']['final'][comp]['img_cls']
            res.extend([self.class2rpo[c] for c in img_cls])    
        return res
    
    def get_image_json(self, image_path, component, camera_id:str, vehicle_type):
        return {
            "image": {
                "path":image_path
                },
            "model": {
                "type": "AOI"
                },
                "info": {
                    "component": component,
                    "camera": camera_id,
                    "vehicleType": vehicle_type
                }
            }

    def _init_model(self, path):
        self._check_files(path)
        #self.predictor = model(path)
        self.predictor = None
        self.predictor.init_model()

    def predict(self, img_json):
        result_json = self.predictor.infer(img_json)
        return result_json

    def _check_files(self, path):
        base_file = 'Base-RCNN-FPN.yaml'
        filename = ['model_final.pth', 'faster_rcnn_R_50_FPN_3x.yaml']
    
        model_dirs = os.listdir(path)
        for model_dir in model_dirs:
            if os.path.isdir(model_dir):
                if model_dir == '__pycache__':
                    continue
                path_dir = os.path.join(path, model_dir) 
                # 基础配置文件
                assert base_file in os.listdir(path_dir), '{} not in package {}'.format(base_file, path_dir)
            
                model_path = os.path.join(path, model_dir, 'model')
                for file in filename: # model file 和配置文件
                    assert file in os.listdir(model_path), '{} not in package {}'.format(file, model_path)
    
    def get_detial_config(self, rpo_lst:list):
        '''
        生成详细配置文件
        '''
        map = {}
        for rpo in rpo_lst:
            map[rpo] = self.map[rpo]
        # 初始化拍摄点位和rpo映射字典
        pos = {}
        for i in range(1, 16):
            pos[i] = []
        # 迭代获取拍摄点位对应rpo
        for key, values in map.items():
            for value in values:
                pos[value].append(key)
        return pos
