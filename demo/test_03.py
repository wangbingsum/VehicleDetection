# 测试脚本，由给定配置文件转到通用配置文件
import xlrd2 as xlrd
import json

def decode(file_path, output_path, config_path, remove_lst=[], map_rpo={}):
    """从给定配置文件中导出通用的配置部分"""
    # 表明给定的这个RPO要去除
    RPO_COL = 2
    # 打开配置文件
    book = xlrd.open_workbook(file_path)
    # 数据默认存放在第一个sheet中
    sheet = book.sheets()[0]
    # 初始化一个保存数据的字典
    data = {}
    # 第三行是package的标题行 4UJ168H03
    for col_index, package in enumerate(sheet.row_values(3)):
        if col_index >= 4 and len(package) == 9:
            data[package] = []
            # 循环package匹配成功的列，提取其中的rpo
            for row_index, is_select in enumerate(sheet.col_values(col_index)):
                if row_index > 3 and is_select in ["x", "X"]:
                    rpo = sheet.col_values(RPO_COL)[row_index].replace("\t", "")
                    if rpo in remove_lst:
                        continue
                    if rpo in map_rpo.keys():
                        data[package].append(map_rpo[rpo])
                    else:
                        data[package].append(rpo)
    
    rpo_set = []
    package_set = []
    packages = {}
    # 从UL的配置文件中读取所有rpo
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        packages = config["packages"]
        # 获取去重的RPO列表进行后续验证
        for package, rpo_lst in config["packages"].items():
            if package not in package_set:
                package_set.append(package)
            for rpo in rpo_lst:
                if rpo not in rpo_set:
                    rpo_set.append(rpo)
    # 输出显示并进行检查
    for key in data.keys():
        if key in package_set:
            print(key)
            rpo_lst = packages[key]
            for rpo in rpo_lst:
                if rpo not in data[key]:
                    print(rpo)
        for rpo in data[key]:
            if rpo not in rpo_set:
                print(f" {rpo}")
    with open(output_path, "w") as f:
        json.dump(data, f)
    print("finish!")
        
if __name__ == "__main__":
    file_UL = r"C:\Users\wangb\Desktop\358 22.5MY Option System20220829.xlsx"
    output_UL = r"output\UL.json"
    config_UL = r"configs\UL.json"
    # 需要进行移除的rpo
    remove_lst = []
    # 表明给定的PRO要进行变换，采用新的进行替代
    map_rpo = {
        "TPX": "VOA",
        "TPV": "VOC",
        "BMK": "B88",
        "YA3": "YA4",
        "E59": "E58"
    }
    # decode(file_UL, output_UL, config_UL, remove_lst, map_rpo)
    file_NB = r"C:\Users\wangb\Desktop\C1UL 23MY Option System20220829.xlsx"
    output_NB = r"output\NB.json"
    config_NB = r"configs\NB.json"
    remove_lst = ["SHF", "UV3", "#19"]
    # 表明给定的PRO要进行变换，采用新的进行替代
    map_rpo = {
        "Q6X": "Q6Y"
    }
    decode(file_NB, output_NB, config_NB, remove_lst, map_rpo)