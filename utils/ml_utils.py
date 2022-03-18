# -*- coding: utf-8 -*-
# @Time    : 2020/10/29 5:08 下午
# @Author  : HuangSir
# @FileName: ml_utils.py
# @Software: PyCharm
# @Desc:

import numpy as np


def prob2Score(prob, basePoint=550, PDO=30, odds=20):
    # 将概率转化成分数且为正整数
    y = np.log(prob / (1 - prob))
    a = basePoint - y * np.log(odds)
    y2 = a - PDO / np.log(2) * (y)
    score = y2.astype('int')
    return score


def cal_ram_rom(df):
    ram_rom = []
    try:
        for i in df.RAM.split('/'):
            if i.endswith('MB'):
                ram_rom.append(float(i.replace('MB', '')) / 1024)
            elif i.endswith('GB'):
                ram_rom.append(float(i.replace('GB', '')))
            else:
                ram_rom.extend([float(i), -999])
        for i in df.ROM.split('/'):
            if i.endswith('MB'):
                ram_rom.append(float(i.replace('MB', '')) / 1024)
            elif i.endswith('GB'):
                ram_rom.append(float(i.replace('GB', '')))
            else:
                ram_rom.extend([float(i), -999])

        return ram_rom
    except Exception as e:
        return 0, 0, 0, 0


def feature_step2(new):
    new['self_3_all']=new[['self_1','self_3']].sum(axis=1)
    new['self_7_all']=new[['self_1','self_3','self_7']].sum(axis=1)
    new['self_15_all']=new[['self_1','self_3','self_7','self_15']].sum(axis=1)
    new['self_30_all']=new[['self_1','self_3','self_7','self_15','self_30']].sum(axis=1)
    new['self_60_all']=new[['self_1','self_3','self_7','self_15','self_30','self_60']].sum(axis=1)
    new['comp_3_all']=new[['comp_1','comp_3']].sum(axis=1)
    new['comp_7_all']=new[['comp_1','comp_3','comp_7']].sum(axis=1)
    new['comp_15_all']=new[['comp_1','comp_3','comp_7','comp_15']].sum(axis=1)
    new['comp_30_all']=new[['comp_1','comp_3','comp_7','comp_15','comp_30']].sum(axis=1)
    new['comp_60_all']=new[['comp_1','comp_3','comp_7','comp_15','comp_30','comp_60']].sum(axis=1)
    new['self_1_pct']=new['self_1']/new['all_self_cnt']
    new['self_3_all_pct']=new['self_3_all']/new['all_self_cnt']
    new['self_7_all_pct']=new['self_7_all']/new['all_self_cnt']
    new['self_15_all_pct']=new['self_15_all']/new['all_self_cnt']
    new['self_30_all_pct']=new['self_30_all']/new['all_self_cnt']
    new['self_60_all_pct']=new['self_60_all']/new['all_self_cnt']
    new['all_self_pct']=new['all_self_cnt']/new['all_cnt']
    new['1_pct']=new['self_1']/new['all_cnt']
    new['3_all_pct']=new['self_3_all']/new['all_cnt']
    new['7_all_pct']=new['self_7_all']/new['all_cnt']
    new['15_all_pct']=new['self_15_all']/new['all_cnt']
    new['30_all_pct']=new['self_30_all']/new['all_cnt']
    new['60_all_pct']=new['self_60_all']/new['all_cnt']
    new['comp_3_pct']=new['comp_3_all']/new['self_3_all']
    new['comp_7_pct']=new['comp_7_all']/new['self_7_all']
    new['comp_15_pct']=new['comp_15_all']/new['self_15_all']
    new['comp_30_pct']=new['comp_30_all']/new['self_30_all']
    new['comp_60_pct']=new['comp_60_all']/new['self_60_all']
    new['all_self_comp_pct']= new['all_self_comp_cnt']/new['all_cnt']
    # add
    new['self_3_add_all']=new[['self_1_add','self_3_add']].sum(axis=1)
    new['self_7_add_all']=new[['self_1_add','self_3_add','self_7_add']].sum(axis=1)
    new['self_15_add_all']=new[['self_1_add','self_3_add','self_7_add','self_15_add']].sum(axis=1)
    new['self_30_add_all']=new[['self_1_add','self_3_add','self_7_add','self_15_add','self_30_add']].sum(axis=1)
    new['self_60_add_all']=new[['self_1_add','self_3_add','self_7_add','self_15_add','self_30_add','self_60_add']].sum(axis=1)
    new['self_3_add_pct']=new['self_3_add_all']/new['lxr_num']
    new['self_7_add_pct']=new['self_7_add_all']/new['lxr_num']
    new['self_15_add_pct']=new['self_15_add_all']/new['lxr_num']
    new['self_30_add_pct']=new['self_30_add_all']/new['lxr_num']
    new['self_60_add_pct']=new['self_60_add_all']/new['lxr_num']
    return new