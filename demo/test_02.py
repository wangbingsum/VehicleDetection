import json

def main(rpo_lst, image_number, rpo_map):
    "生成详细配置文件"
    map = {}
    for rpo in rpo_lst:
        map[rpo] = rpo_map[rpo]
    # 初始化拍摄点位和rpo映射字典
    pos = {}
    for i in range(1, image_number + 1):
        pos[i] = []
    # 迭代获取拍摄点位对应rpo
    for key, values in map.items():
        for value in values:
            pos[value].append(key)
                    
    return pos
    
if __name__ == "__main__":
    with open("configs/NL.json", "r") as f:
        config = json.load(f)
    rpo_map = config["rap_map"]
    packages = config["packages"]
    rpo_lst = packages["6NL268V43"]
    main()