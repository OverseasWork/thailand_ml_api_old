# -*- coding: utf-8 -*-
# @Time    : 2021/11/6 11:35 下午
# @Author  : HuangSir
# @FileName: ml_router.py
# @Software: PyCharm
# @Desc: 新老客模型路由


from fastapi import APIRouter

from app.app.cust_ml.core import CustData
from app.app.cust_ml import risk_score


ml_router = APIRouter()


@ml_router.post('/customer/score', tags=['客户信用评分'])
async def cust_risk_score(data: CustData):
    data = data.dict()
    res = risk_score(data)
    return res