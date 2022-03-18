import pandas as pd
import numpy as np
import re
import json
import joblib
import datetime
from conf.log_config import log
from utils.load_utils import load_txt_feat
from utils.ml_utils import prob2Score, cal_ram_rom, feature_step2

import sys
sys.path.append('..')

path = 'app/app/cust_ml/static/'

comp = pd.read_excel(f'{path}comp.xlsx')


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


def risk_score(data: dict):
    try:
        busiId = data['busi_id']
    except:
        busiId = None
    if len(data) <= 1 or busiId is None:
        log.logger.warning(f'{busiId}:Data is empty --------------------------------')
        return {'prob': -9999, 'status_code': 101, 'msg': 'success',
                'detail': '参数错误', 'version': '3.0'}
    try:
        # 主函数
        log.logger.info(f'{busiId}: starting run --------------------------------')
        data['add_list'] = json.dumps(data['add_list'])
        data['app_list'] = json.dumps(data['app_list'])
        a = json.dumps(data)
        data = pd.DataFrame(json.loads(a), index=[0])

        data[['ram_x', 'ram_y', 'rom_x', 'rom_y']] = data.apply(cal_ram_rom, result_type="expand", axis=1)
        data2 = get_feature(data.reset_index(drop=True))
        feature_step2(data2)
        data3 = pd.merge(
            data[['busi_id', 'create_time', 'face_comparison', 'campaign_name', 'channel', 'loan_market', 'is_new',
                  'ram_x', 'rom_x', 'current_debt_amount', 'kids', 'industry', 'education', 're_24h_apply_num',
                  're_7d_apply_num', 'his_sum_rej_cnt', 'age', 'device_cor_mobile_num', 'identity_cor_mobile_num',
                  'identity_register_product', 'income', 'phone_version_num', 'gender', 'work_type', ]], data2, on='busi_id', how='right')

        # 老客
        if all(data3['is_new'] == 0):
            lgb_model = joblib.load(f"{path}tail_old_0316.pkl")
            in_model_col = load_txt_feat(f"{path}old_in_model_col.txt")
            campaign_name_map = {'adrachel': 0, 'superads': 1, 'neptune': 2, 'bojan': 3, 'Organic': 4,
                                 'fendikennytech': 5, 'Cash': 6, 'ahajoyco': 7, 'API': 8,
                                 -999: 9, 'adsnova': 10, 'AdRachel': 11, 'hamobi': 12, 'xinmiaohudong': 13,
                                 'chestnuts': 14, 'Cash2': 15, 'lookflyer': 16}

            model_data = data3[in_model_col]
            model_data['campaign_name'] = model_data.apply(lambda x: campaign_name_map.get(x['campaign_name'], 9),
                                                           axis=1)
            lgb_prob = np.mean([i.predict(model_data) for i in lgb_model], axis=0)[0]
            score = prob2Score(lgb_prob)
            result = {'prob': int(score), 'msg': 'success', 'status_code': 100, 'busiId': busiId, 'version': '3.0'}
            log.logger.info(f'{busiId}:finish predict,score:{int(score)}, '
                            f'[old customer]--------------------------------')
        # 新客
        else:
            lgb_model = joblib.load(f"{path}tail_new_0316.pkl")
            in_model_col = load_txt_feat(f"{path}new_in_model_col.txt")
            campaign_name_map = {
                'superads': 0, 'adrachel': 1, 'Organic': 2, 'Cash': 3, 'bojan': 4, 'ahajoyco': 5, -999: 6,
                'neptune': 7, 'fendikennytech': 8, 'API': 9, 'xinmiaohudong': 10, 'adsnova': 11, 'AdRachel': 12,
                'hamobi': 13,
                'chestnuts': 14, 'Cash2': 15
            }
            channel_map = {
                'Facebook': 0, 'Cash': 1, 'Organic': 2, -999: 3, 'Google': 4,
                'bojan': 5, 'bytedanceglobal_int': 6, 'AdRachel': 7, 'Cash2': 8
            }
            model_data = data3[in_model_col]
            model_data['campaign_name'] = model_data.apply(lambda x: campaign_name_map.get(x['campaign_name'], 6),
                                                           axis=1)
            model_data['channel'] = model_data.apply(lambda x: channel_map.get(x['channel'], 3), axis=1)
            lgb_prob = np.mean([i.predict(model_data) for i in lgb_model], axis=0)[0]
            score = prob2Score(lgb_prob)
            result = {'prob': int(score), 'msg': 'success', 'status_code': 100, 'busiId': busiId, 'version': '3.0'}
            log.logger.info(f'{busiId}:finish predict,score:{int(score)}, '
                            f'[new customer]--------------------------------')
        return result
    except Exception as error:
        log.logger.error(f'{busiId},-----> {str(error)}')
        return {'busiId': busiId, 'status_code': 102, 'msg': 'fail', 'detail': str(error), 'version': '3.0'}




