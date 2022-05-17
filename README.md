# VehicleDetection

### 进度
> 1. 配置文件生成(已完成)
> 2. 参数加载(已完成)
> 3. 模型调用(已完成)
> 4. 解码判断检测结果(已完成)
> 5. 生成检测报告(已完成)
> 6. 检测报告区分高配和低配车型，进行单独存放(已完成)
> 6. 程序兼容不同车型的配置(已完成)
> 7. 剩余运行时间估算(已完成)
> 8. 邮件提示程序运行结果
> 9. 增加检测结果分析程序

### 使用方法

1. 安装
~~~ bash
# 在本项目根目录进行安装
pip install -e .
~~~

2. 使用

~~~ python
from vehicle_detection.api import load_image
from vehicle_detection.core.predict import VehicleDetector

# 以358为例
# 1. 检测图片加载
img_lst = load_image(image_root_dir="home/jovyan/data", model_name="358", image_number=16)

# 2. 检测器初始化
detector = VehicleDetector(config="home/jovyan/configs/358/UL.json", model_name="358", vehicles=img_lst)

# 3. 模型初始化(避免模型对应的predict.py来回复制, 所以在外部进行模型初始化)
from predict import model

predictor = model("{checkpoint path}")
predictor.init_model()

# 3. 执行检测流程
# result: OK -> [{vin}, {package}, {PIC{i}}, "OK", " ", " ", ...]
#         NG -> [{vin}, {package}, {PIC{i}}, "NG", {description}, {image_path}, ...]
result = detector.run(predictor)
~~~