# -*- encoding: utf-8 -*-
'''
@Description:对检测结果进行简单分析
@Date       :2022/05/17 19:48:55
@Author     :wangbing
@version    :1.0
'''

from tqdm import tqdm


__all__ = ["analyse_result"]


def analyse_result(result):
    pass_count = 0
    
    for res in tqdm(result):
        if res[2] == "OK":
            pass_count += 1
    print(f"pass: {pass_count / len(result) * 100 :04f}%({pass_count}/{len(result)})")