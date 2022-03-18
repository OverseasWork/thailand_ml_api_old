# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 3:58 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc:

from pydantic import BaseModel, Field
from typing import List
from app.app.applist_ml.core import AppList, AddList, appListExample, addListExample


class CustData(BaseModel):
    # 客户数据模型
    busi_id: str = Field(default='1020210717125639000083595', title='交易订单号')
    create_time: str = Field(default=None, title='订单时间', example='2022-01-06 09:39:24',
                            description='yyyy-mm-dd HH:MM:SS')
    RAM: str = Field(default=None, title='RAM', example='564 MB/2.77 GB')
    ROM: str = Field(default=None, title='ROM', example='38.60 GB/53.11 GB')
    work_type: int = Field(default=None, title='职位', example=1,
                           description='1:正式员工(2年以下); 2:正式员工(2年以上); 3:经理; 4:高管; 5:外包; 6:临时合同工')
    education: int = Field(default=None, title='教育程度', example=5,
                           description='1:小学、2:初中、3:高中 4:大专、 5:本科、6:其他')
    loan_market: int = Field(default=None, title='是否贷超', example=1, description='1表示贷超，0表示非贷超')
    is_new: int = Field(title='是否新客', example=1, description='1 表示新客，0 表示老客')
    re_24h_apply_num: int = Field(default=None, title='近24小时申请次数', example=0, description='0,1,2,3 ...')
    age: int = Field(default=None, title='年龄', example=35, description="下单时间减去 - 出生日期")
    his_sum_rej_cnt: int = Field(default=None, title='历史累计拒绝次数', example=0)
    gender: str = Field(default=None, title='性别', example='MALE', description='性别:MALE,FEMALE')
    campaign_name: str = Field(default=None, title='渠道名', example='adrachel')
    kids: int = Field(default=0, title='孩子个数', example=1)
    current_debt_amount: float = Field(default=None, title='当前共债金额', example=1000.0)
    industry: int = Field(default=None, title='行业', example=59)
    face_comparison: int = Field(default=None, title='人脸比对', example=77)
    channel: str = Field(default=None, title='渠道名', example='Facebook')
    device_cor_mobile_num: int = Field(default=None, title='设备关联手机号数量', example=2)
    identity_cor_mobile_num: int = Field(default=None, title='身份证关联手机号数量', example=2)
    identity_register_product: int = Field(default=None, title='身份证注册过的产品数量', example=1)
    re_7d_apply_num: int = Field(default=0, title='近7天申请次数', example=0, description='0,1,2,3 ...')
    phone_version_num: int = Field(default=None, title='手机版本号', example=10)
    income: float = Field(default=None, title='收入', example=3000.0)
    ram_x: float = Field(default=None, title='RAM_X', example=16.25, description='RAM: 3.25 GB/8.01 GB, 截取第一个数值')
    rom_x: float = Field(default=None, title='ROM_X', example=18.01, description='RAM: 3.25 GB/128 GB, 截取第一个数值')
    app_list: List[AppList] = Field(default=..., example=appListExample, title='appList', description='applist详情')
    add_list: List[AddList] = Field(default=..., example=addListExample, title='通讯录', description='通讯录详情')
