# -*- encoding: utf-8 -*-
'''
@Description:保存检测结果
@Date       :2022/05/18 09:20:10
@Author     :wangbing
@version    :1.0
'''


__all__ = ["save_result"]


def save_result(save_path, result):
    with open(save_path, 'w', encoding='utf-8') as writer:
        for vehicle in result:
            write_data = ','.join(vehicle)
            writer.write(write_data)
            writer.write('\n')