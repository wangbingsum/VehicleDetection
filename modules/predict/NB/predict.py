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
        self.class_names = {'model1':['12_dummy_tire', '28t_logo', '3_level_panel', 'AWD_logo', 'XT5_logo', 'big_sensor', 
          'black_roof_rail', 'black_win_molding', 'bright_grille', 'bright_rock_mold', 
          'bright_roof_rail', 'bright_win_molding', 'dick_one_camera', 'dick_two_camera', 
          'front_4_radars', 'lighting_dh', 'rear_4_radars', 'red_tail_light', 
          'sgm_logo', 'sliver_front_molding', 'sliver_rear_molding',
          'sliver_roof_rail', 'small_hud', 'two_roof_win'],
                        }
        
        self.com_dict = {'model1':{'bright_grille':'格栅', 'sporty_grille':'格栅', '3_level_panel':'三格栅', 'LRR':'中间饰盖', 
                                  'NV':'夜视', 'black_front_molding':'前保饰板', 'sliver_front_molding':'前保饰板', 
                                   'no_rear_molding':'后保饰板','sliver_rear_molding':'后保饰板', 'Pianoblack_rear_molding':'后保饰板', 
                                  'one_roof_win':'天窗', 'two_roof_win':'天窗', 'logo_camara':'前保摄像头',
                                  '12_alloy_tire':'轮毂', '12_dummy_tire':'轮毂', '12_fork_tire':'轮毂',
                                  '12_sporty_tire':'轮毂', '12_paralled_tire':'轮毂', '24_tire':'轮毂',
                                  'chrome_dh':'门把手', 'lighting_dh':'门把手', 'sameColor_dh':'门把手',
                                  'bright_rock_mold':'门下饰条', 'red_tail_light':'尾灯', 'white_tail_light':'尾灯',
                                  'dick_one_camera':'后盖', 'dick_two_camera':'后盖',
                                  'AWD_logo':'下标牌', '28t_logo':'上标牌', 'XT5_logo':'上标牌','sgm_logo':'下标牌', 
                                  'front_4_radars':'前保雷达', 'front_6_radars':'前保雷达',
                                  'rear_4_radars':'后保雷达', 'rear_6_radars':'后保雷达', 
                                   'small_hud':'前挡玻璃', 'big_hud':'前挡玻璃',
                                   'small_sensor':'传感器', 'big_sensor':'传感器',
                                   'bright_roof_rail':'行李架', 'black_roof_rail':'行李架', 'sliver_roof_rail':'行李架',
                                   'bright_win_molding':'窗饰条', 'black_win_molding':'窗饰条'
                                  }
                        }
        
        self.com_vi = {'前保下端':['三格栅', '中间饰板', '夜视'], '前保饰板':['前保饰板'], '后保饰板':['后保饰板'],
                       '格栅':['格栅'], '前保摄像头':['前保摄像头'],
                      '前左轮毂':['轮毂'], '前右轮毂':['轮毂'], '后左轮毂':['轮毂'], 
                       '后右轮毂':['轮毂'], '天窗':['天窗'],
                      '左前门把手':['门把手'], '右前门把手':['门把手'], '左后门把手':['门把手'], '右后门把手':['门把手'],
                       '左门下饰条':['门下饰条'], '右门下饰条':['门下饰条'],
                       '左尾灯':['尾灯'], '右尾灯':['尾灯'],'后盖':['后盖'], '标牌':['上标牌','下标牌'],
                       '左前保雷达':['雷达'], '右前保雷达':['雷达'],'左后保雷达':['雷达'], '右后保雷达':['雷达'], 
                       '前挡玻璃':['前挡玻璃'], '传感器':['传感器'], '左行李架':['行李架'], '右行李架':['行李架'], 
                      '左窗饰条':['窗饰条'], '右窗饰条':['窗饰条']}
        
        
        self.no_type = {'左后保雷达':'rear_4_radars', '右后保雷达':'rear_4_radars',
                        '左前保雷达':'front_4_radar', '右前保雷达':'front_4_radar',
                        '天窗':'one_roof_win'}
        
        
    def init_model(self):
        
        model1 = os.path.join(self.root, 'model1', 'model', "model_final.pth")
        config1 = os.path.join(self.root, 'model1', 'model', "faster_rcnn_R_50_FPN_3x.yaml")
        self.predictor1, self.cfg1 = self.get_model(model1, config1, 0.3, self.class_names['model1'])
        
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
            detectron_pred = self.predictor1(img)
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
        

        class_names = self.class_names['model1']
        com_dict = self.com_dict['model1']
            
        instances = pred['instances']
        scores = instances.get_fields()["scores"].tolist()
        pred_classes = instances.get_fields()["pred_classes"].tolist()
        print(pred_classes)
        pred_class_names = list(map(lambda x:class_names[x], pred_classes))
        pred_component = list(map(lambda x:com_dict[x], pred_class_names))
        pred_boxes = instances.get_fields()["pred_boxes"].tensor.tolist()
        
        print(pred_class_names)
        print(pred_component)
        
        for comp in component:         
            comp_in_model = self.com_vi[comp]
            
            cls = []
            box = []
            score = []
            for item in comp_in_model:
                ret_tmp = []
                try:
                    for i in range(len(pred_component)):
                        if pred_component[i] == item:
                            ret_tmp.append(i)
                            
                    if ret_tmp:
                        cls.append(pred_class_names[ret_tmp[0]])
                        box.append(pred_boxes[ret_tmp[0]])
                        score.append(scores[ret_tmp[0]])
                        
                except Exception as e:
                    self.dump_error_result(630, e)
                    continues
                    
            if len(cls) >= 1:  
                self.result['result']['final'][comp]['img_cls'] = cls
                self.result['result']['final'][comp]['img_box'] = box
                self.result['result']['final'][comp]['img_score'] = score
            elif comp in self.no_type.keys(): # no_hud等模型未学习输出
                self.result['result']['final'][comp]['img_cls'] = [self.no_type[comp]]
                self.result['result']['final'][comp]['img_box'] = [None]
                self.result['result']['final'][comp]['img_socre'] = [None]
             
        return