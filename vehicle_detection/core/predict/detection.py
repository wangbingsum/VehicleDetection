'''
@Description:检测器
@Date       :2021/08/30 08:50:43
@Author     :wangbing
@version    :1.0
'''

import os
from tqdm import tqdm
import json

class VehicleDetector:
    def __init__(self, config, model_name:str, vehicles:list):
        super().__init__()
        if isinstance(config, str):
            config = self.load_config(config)
        self.map = config['rpo_map'] # rpo到拍摄位置的映射
        self.packages = config['packages'] # 车型配置
        self.class2rpo = config['class_to_rpo'] # 英文类别到rpo的映射
        self.rpo2description = config['rpo_to_description'] # rpo到中文的映射
        self.componets = config['componets']
        self.config = config['config']
        self.image_number = self.config['image_number']
        self.model_name = model_name # 当前检测的模型
        self.vehicles = vehicles # 检测车辆信息列表

    def load_config(self, path):
        with open(path, "r") as f:
            config = json.load(f)
        return config
    
    def run(self, model=None):
        print(f'当前检测车型：{self.model_name}')
        if model is None:
            print("深度学习模型初始化中...")
            # 兼容不同模型版本
            model_path = self.config['model_path']['latest']
            res = self._init_model(model_path)
            if res == False: 
                print("模型初始化异常")
                return
        else:
            self.predictor = model

        detection_results = []
        for vehicle in tqdm(self.vehicles):
            try:
                # 轮询检测每一张图片
                rpos = self.packages[vehicle.package]
                # 获取当前配置下每个拍摄位置对应的rpo列表
                pos_config = self.get_detial_config(rpos, self.image_number)
                result = []
                result.append(vehicle.vin)
                result.append(vehicle.vehicle_package)
                for i in range(1, len(vehicle) + 1):
                    result.append(f"PIC{i}")
                    image_path = vehicle[i]
                    componet = self.componets[str(i)]
                    # 构造调用json文件
                    image_json = self.get_image_json(image_path, componet, i, self.model_name)
                    # 调用模型
                    result_json = self.predict(image_json)
                    # 解码得到当前拍摄位置的预测类别信息
                    predict_cls = self.decode(componet, result_json)
                    # 对比配置文件和预测信息，获取检测结果
                    res = self.compare(i, pos_config[i], predict_cls, rpos, vehicle.vehicle_package)
                    if res != 'OK':
                        # 添加保存调用图像图像地址
                        result.extend(['NG', res, image_path])
                    else:
                        result.extend(['OK', ' ', ' '])
                # 插入一辆车总的检测结果
                if 'NG' in result:
                    result.insert(2, 'NG')
                else:
                    result.insert(2, 'OK')
                detection_results.append(result)
            except Exception as e:
                print(f'error message: {e}')
        return detection_results
    
    def compare(self, position, acutal:list, predict:list, rpo_lst:list, package:str):
        '''比对预测类别和实际类别，得到预测结果
            1. 预测数量不相等
            2. 预测类别不相等'''
        
        if self.model_name == "C1TL":
            if position in [11, 14]:
                # 单独处理pacakge中包含V39和V40的车型
                if "V39" in package or "V40" in package:
                    predict = [rpo for rpo in predict if rpo != "UD5"]
                    acutal = [rpo for rpo in acutal if rpo != "UD5"]
                # 单独处理RPO中包含UKG的车型
                if "UKG" in rpo_lst:
                    if "UD5" in predict and "UD5" in acutal:
                        # TODO: 对高配车型的11和14点位进行处理
                        pass
        if len(acutal) == 0:
            return 'OK'
        pre = ' '.join(predict)
        acu = ' '.join(acutal)
        if len(predict) != len(acutal):
            return f'position: {position} Unequal quantity: actual: {acu} predict: {pre}'
        elif not self._check_element_equal(predict, acutal):
            return f'position: {position} Class inequality: actual: {acu} predict: {pre}'
        else:
            return 'OK'
            
    def _check_element_equal(self, predict, actual):
        "对预测类别和实际类别进行相等性判断"
        for pre in predict:
            if pre not in actual: return False
        return True

    def decode(self, componet, result_json): 
        "返回当前拍摄位置，预测到的所有类别信息"
        res = []
        for comp in componet:
            img_cls = result_json['result']['final'][comp]['img_cls']
            res.extend([self.class2rpo[c] for c in img_cls if c != None])    
        return res
    
    def get_image_json(self, image_path, component, camera_id:str, vehicle_type):
        "获取模型调用json文件"
        return {
            "image": {
                "path":image_path
                },
            "model": {
                "type": "AOI"
                },
                "info": {
                    "component": component,
                    "camera": str(camera_id),
                    "vehicleType": vehicle_type
                }
            }

    def _init_model(self, path):
        self._check_files(path)
        if self.model_name == "358":
            from ..models.UL.predict import model
        elif self.model_name == "C1UL":
            from ..models.NB.predict import model
        elif self.model_name == "E2UL":
            from ..models.ZK.predict import model
        elif self.model_name == "C1TL":
            from ..models.NL.predict import model
        elif self.model_name == "O1":
            from ..models.KR.predict import model
        else:
            #self.predictor = None
            return False
        
        self.predictor = model(path)
        #self.predictor = None
        self.predictor.init_model()
        return True

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
    
    def get_detial_config(self, rpo_lst:list, image_number):
        "生成详细配置文件"
        map = {}
        for rpo in rpo_lst:
            map[rpo] = self.map[rpo]
        # 初始化拍摄点位和rpo映射字典
        pos = {}
        for i in range(1, image_number + 1):
            pos[i] = []
        # 迭代获取拍摄点位对应rpo
        for key, values in map.items():
            for value in values:
                pos[value].append(key)
                    
        return pos
