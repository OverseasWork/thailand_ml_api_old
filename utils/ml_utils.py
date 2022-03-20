# -*- coding: utf-8 -*-
# @Time    : 2020/10/29 5:08 下午
# @Author  : HuangSir
# @FileName: ml_utils.py
# @Software: PyCharm
# @Desc:

import numpy as np
import pandas as pd
import json, re
import datetime


path = 'app/app/cust_ml/static/'

comp = pd.read_excel(f'{path}comp.xlsx')


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


def get_feature(data):
    df = pd.DataFrame(json.loads(data.loc[0, 'app_list']))
    df['apply_time'] = data.loc[0, 'create_time']
    df['apply_time'] = pd.to_datetime(df['apply_time'])
    df['lastTime'] = pd.to_datetime(df['lastTime'])
    self_df = df[df.lastTime > datetime.datetime(2010, 1, 1)]

    day_tag = pd.DataFrame(pd.cut((self_df['apply_time'] - self_df['lastTime']).dt.days,
                                  bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                  labels=['self_1', 'self_3', 'self_7', 'self_15', 'self_30', 'self_60',
                                          'self_90']).value_counts()).T
    day_tag.columns = day_tag.columns.tolist()
    self_comp = df[df.packageName.isin(comp.package)]
    comp_day_tag = pd.DataFrame(pd.cut((self_comp['apply_time'] - self_comp['lastTime']).dt.days,
                                       bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                       labels=['comp_1', 'comp_3', 'comp_7', 'comp_15', 'comp_30', 'comp_60',
                                               'comp_90']).value_counts()).T
    comp_day_tag.columns = comp_day_tag.columns.tolist()
    day_tag['busi_id'] = data.loc[0, 'busi_id']
    # day_tag['DB'] = data.loc[0, 'db_name']
    day_tag['apply_time'] = data.loc[0, 'create_time']
    day_tag['all_self_cnt'] = self_df.shape[0]
    day_tag['all_self_comp_cnt'] = self_comp.shape[0]
    day_tag['all_cnt'] = df.shape[0]
    # add-------
    add_df = pd.DataFrame(json.loads(data.loc[0, 'add_list']))
    add_df['contain_chs'] = add_df['other_name'].str.extract(r'([\u4e00-\u9fa5]+)')
    lxr_num = add_df.shape[0]
    chs_lxr_num = add_df[~add_df.contain_chs.isnull()].shape[0]
    cnt = 0
    for j in add_df.other_mobile.tolist():
        if re.match('^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', '%s' % j):
            cnt += 1

    add_df['apply_time'] = data.loc[0, 'create_time']
    add_df['apply_time'] = pd.to_datetime(add_df['apply_time'])
    try:
        add_df['last_time'] = pd.to_datetime(add_df['last_time'])
        add_day_tag = pd.DataFrame(pd.cut((add_df['apply_time'] - add_df['last_time']).dt.days,
                                          bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                          labels=['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add',
                                                  'self_30_add', 'self_60_add', 'self_90_add']).value_counts()).T
        add_day_tag.columns = add_day_tag.columns.tolist()
    except Exception as e:
        add_df['last_time'] = '2000-01-01 00:00:01'
        add_df['last_time'] = pd.to_datetime(add_df['last_time'])
        add_day_tag = pd.DataFrame(pd.cut((add_df['apply_time'] - add_df['last_time']).dt.days,
                                          bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                          labels=['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add',
                                                  'self_30_add', 'self_60_add', 'self_90_add']).value_counts()).T
        add_day_tag.columns = add_day_tag.columns
        add_day_tag.loc[0, :] = -999

    add_day_tag[['lxr_num', 'chs_lxr_num', 'cnt']] = [lxr_num, chs_lxr_num, cnt]
    all_tag = pd.concat([day_tag, add_day_tag, comp_day_tag], axis=1)
    return all_tag
