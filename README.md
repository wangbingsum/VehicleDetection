# VehicleDetection

### 开发日志
2022-05-17
> 1. 添加适用于单个模型预测的API

2022-05-31
> 1. 修改NL的配置文件,增加UD0(前保无雷达)的配置

### 使用方法

1. 安装
~~~ bash
# 在本项目根目录进行安装
pip install -e .
~~~

2. 使用

~~~ python
from vehicle_detection.api import load_image, analyse_result, save_result
from vehicle_detection.core.predict import VehicleDetector

# 以358为例
# 1. 检测图片加载
img_lst = load_image(image_root_dir="/home/jovyan/data", model_name="358", image_number=16)

# 2. 检测器初始化
detector = VehicleDetector(config="/home/jovyan/configs/358/UL.json", model_name="358", vehicles=img_lst)

# 3. 模型初始化(避免模型对应的predict.py来回复制, 所以在外部进行模型初始化)
from predict import model

predictor = model("{checkpoint path}")
predictor.init_model()

# 4. 执行检测流程
# result: OK -> [{vin}, {package}, {PIC{i}}, "OK", " ", " ", ...]
#         NG -> [{vin}, {package}, {PIC{i}}, "NG", {description}, {image_path}, ...]
result = detector.run(predictor)

# 5. 检测结果分析
analyse_result(result)

# 6. 保存检测结果
save_result("{save path}", result)
~~~