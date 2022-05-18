from vehicle_detection.api import load_image, analyse_result, save_result
from vehicle_detection.core import VehicleDetector
from predict import model

def test(image_root_dir, mode_name, image_number, cfg_path, cp_path):
    
    # 1. 检测图片加载
    img_lst = load_image(image_root_dir=image_root_dir, model_name=mode_name, image_number=image_number)

    # 2. 检测器初始化
    detector = VehicleDetector(config=cfg_path, model_name=mode_name, vehicles=img_lst)

    # 3. 模型初始化(避免模型对应的predict.py来回复制, 所以在外部进行模型初始化)
    predictor = model(cp_path)
    predictor.init_model()

    # 4. 执行检测流程
    # result: OK -> [{vin}, {package}, {PIC{i}}, "OK", " ", " ", ...]
    #         NG -> [{vin}, {package}, {PIC{i}}, "NG", {description}, {image_path}, ...]
    result = detector.run(predictor)

    # 5. 检测结果分析
    analyse_result(result)

    save_result("result.csv", result)
        
    return result

if __name__ == "__main__":
    image_root_dir = ""
    mode_name = ""
    image_number = 16
    cfg_path = ""
    cp_path = ""
    test(image_root_dir, mode_name, image_number, cfg_path, cp_path)