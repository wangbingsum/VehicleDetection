# -*- coding: utf-8 -*-
"""
Leo Editor

model_api
"""
import torch
import os
import json
import cv2
import numpy as np
import random
import requests
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

class model:
    
    def __init__(self, root_path):
         
        self.root = root_path
        self.class_names = {'model2':['10_light_tire', '10_polish_tire', '15_tire', '20_tire', '653t', 
                                      'avenir_geshan', 'avenir_logo', 'big_camara', 'big_hud', 
                                      'big_sensor', 'chrome_dh', 'dick_wo_camara', 
                                      'double_window', 'front_6_radars', 'gl8_es_logo',
                                      'gl8_logo', 'high_tail_light', 'logo',
                                      'logo_camara', 'low_tail_light', 'no_hud', 'no_logo', 
                                      'no_sensor', 'normal_geshan', 
                                      'normal_light', 'rear_6_radars', 'rock_mold', 
                                      'sameColor_dh', 'sgm_logo',
                                      'side_label', 'single_window', 'small_camara', 
                                      'small_hud', 'small_sensor', 'wavy_light'],
                            'model1':['normal_light', 'wavy_light']}
        
        self.com_dict = {'model2':{'10_light_tire': '轮毂', '10_polish_tire': '轮毂', 
                                   '15_tire': '轮毂',  '20_tire': '轮毂', '653t': '上标牌', 
                                   'avenir_geshan': '格栅', 'avenir_logo': '上标牌', 
                                   'big_camara': '后盖', 'big_hud': '前挡玻璃',
                                   'big_sensor': '传感器', 'chrome_dh': '门把手', 
                                   'dick_wo_camara': '后盖', 'double_window': '天窗', 
                                   'front_6_radars': '雷达','normal_light': '大灯', 
                                   'gl8_es_logo': '下标牌','gl8_logo': '下标牌', 
                                   'high_tail_light': '尾灯', 'logo': '罩盖',
                                   'logo_camara': '前保摄像头','low_tail_light': '尾灯',
                                   'no_hud': '前挡玻璃', 'no_logo': '罩盖', 
                                   'no_sensor': '传感器', 'normal_geshan': '格栅',
                                   'rear_6_radars': '雷达', 'rock_mold': '门下饰条', 
                                   'sameColor_dh': '门把手', 'sgm_logo': '下标牌', 
                                   'side_label': '标签', 'single_window': '天窗',
                                   'small_camara': '后盖',  'small_hud': '前挡玻璃',
                                   'small_sensor': '传感器', 'wavy_light': '大灯'},
                        'model1':{'normal_light':'大灯', 'wavy_light':'大灯'}}
        
        self.com_vi = {'左大灯':['大灯'], '右大灯':['大灯'], '罩盖':['罩盖'],
                       '格栅':['格栅'], '前保摄像头':['前保摄像头'],
                      '前左轮毂':['轮毂'], '前右轮毂':['轮毂'], '后左轮毂':['轮毂'], 
                       '后右轮毂':['轮毂'], '天窗':['天窗'],
                      '左门把手':['门把手'], '右门把手':['门把手'],
                       '门下饰条':['门下饰条'], '左尾灯':['尾灯'], 
                       '右尾灯':['尾灯'],'后盖':['后盖'], '标牌':['上标牌','下标牌'],
                       '前保雷达':['雷达'],  '左后保雷达':['雷达'], '右后保雷达':['雷达'], 
                       '前挡玻璃':['前挡玻璃'], '传感器':['传感器'], '标签':['标签']}
        
        self.no_type = {'左后保雷达':'rear_4_radars', '右后保雷达':'rear_4_radars',
                        '前挡玻璃':'no_hud', '传感器':'no_sensor',
                       '标签':'no_side_label', '后盖':'dick_wo_camara', 
                        '门下饰条':'no_rock_mold', '天窗':'single_window',
                       '前保摄像头':'no_logo_camara','前保雷达':'no_front_radar'}
        
        
    def init_model(self):
        
        model1 = os.path.join(self.root, 'model1', 'model', "model_final.pth")
        config1 = os.path.join(self.root, 'model1', 'model', "faster_rcnn_R_50_FPN_3x.yaml")
        self.predictor1, self.cfg1 = self.get_model(model1, config1, 0.3, self.class_names['model1'])
        
        model2 = os.path.join(self.root, 'model2', 'model', "model_final.pth")
        config2 = os.path.join(self.root, 'model2', 'model', "faster_rcnn_R_50_FPN_3x.yaml")
        self.predictor2, self.cfg2 = self.get_model(model2, config2, 0.3, self.class_names['model2'])
        
        return

    
    def get_model(self, model, config_file, threshold, class_names):
        cfg = get_cfg()
        cfg.merge_from_file(config_file)
#         print(model)
        cfg.MODEL.WEIGHTS = model
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(class_names)  
        cfg.MODEL.DEVICE = 'cuda'
        
        return DefaultPredictor(cfg), cfg
    
    
    def infer(self, img_json):
        
        self.result = self.create_result_dict(img_json['info'])
        
        #read image
        try:
            img_path = img_json['image']['path']
            info = img_json['info']
            component = info['component']
            img = cv2.imread(img_path)
            assert img is not None, "Cannot get image or CAM!"
        except Exception as e:
            self.dump_error_result(610, e)

#         component = list(map(lambda x:self.com_vi[x], component))
#         print(component)
        #infer image
        try:
            if '左大灯' in component or '右大灯' in component:
                detectron_pred = self.predictor1(img)
            else:
                detectron_pred = self.predictor2(img)
        except Exception as e:
            self.dump_error_result(620, e)
        
        #post process
        self.post_process(detectron_pred, component)
        
        
        return self.result 
    
    def pre_process(self, img):
        """
        如有需要可对图片进行预处理
        :param img:
        :return:
        """
        processed_img = img
        return processed_img   
    
    def create_result_dict(self, info):
        # 生成结果基础格式 
        component = info['component']
        result = {}
        result.setdefault('message', "success")
        result.setdefault('status', 200)
        result.setdefault('result',{})
        result['result'].setdefault('final', {})
          
        for p in component:
            rr= {}
            rr.setdefault('img_cls', [])
            rr.setdefault('img_box', [])
            rr.setdefault('img_score', [])
            result['result']['final'].setdefault(p, rr)
        result['result']['final'].setdefault('message', 'success')
        result['result']['final'].setdefault('status', 200)
            
        return result.copy()
    
    def dump_error_result(self,  code, message):
        # 异常处理
        self.result["status"] = code
        if not isinstance(message, str):
            message = repr(message)
        self.result["message"] = message    
    
    def post_process(self, pred, component):
        
        if '左大灯' in component or '右大灯' in component:
            class_names = self.class_names['model1']
            com_dict = self.com_dict['model1']
        else:
            class_names = self.class_names['model2']
            com_dict = self.com_dict['model2']
            
        instances = pred['instances']
        scores = instances.get_fields()["scores"].tolist()
        pred_classes = instances.get_fields()["pred_classes"].tolist()
        pred_class_names = list(map(lambda x:class_names[x], pred_classes))
        pred_component = list(map(lambda x:com_dict[x], pred_class_names))
        pred_boxes = instances.get_fields()["pred_boxes"].tensor.tolist()
        
        print(pred_class_names)
        print(pred_component)
        
        for comp in component:         
            comp_in_model = self.com_vi[comp]
            
            clf = []
            box = []
            score = []
            for item in comp_in_model:
                ret_tmp = []
                try:
                    for i in range(len(pred_component)):
                        if pred_component[i] == item:
                            ret_tmp.append(i)
                            
                    if ret_tmp:
                        clf.append(pred_class_names[ret_tmp[0]])
                        box.append(pred_boxes[ret_tmp[0]])
                        score.append(scores[ret_tmp[0]])
                        
                except Exception as e:
                    self.dump_error_result(630, e)
                    continue
                    
            if len(clf) >= 1:  
                self.result['result']['final'][comp]['img_cls'] = clf
                self.result['result']['final'][comp]['img_box'] = box
                self.result['result']['final'][comp]['img_score'] = score
            elif comp in self.no_type.keys(): # no_hud等模型未学习输出
                self.result['result']['final'][comp]['img_cls'] = [self.no_type[comp]]
                self.result['result']['final'][comp]['img_box'] = [None]
                self.result['result']['final'][comp]['img_socre'] = [None]
             
        return