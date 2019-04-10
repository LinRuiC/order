# -*- coding: utf-8 -*-
from application import  app,db
from flask import Blueprint
from common.libs.Helper import ops_render
from common.libs.Helper import getFormatDate
from common.models.stat.StatDailySite import StatDailySite
import datetime
route_index = Blueprint( 'index_page',__name__ )

# 仪表盘
@route_index.route("/")
def index():
    resp_data = {
        'data':{
            # 营收概况
            'finance':{
                'today':0,
                'month':0
            },
            # 会员
            'member': {
                'today_new': 0,
                'month_new': 0,
                'total': 0
            },
            # 订单
            'order': {
                'today': 0,
                'month': 0
            },
            # 分享
            'shared': {
                'today': 0,
                'month': 0
            },
        }
    }

    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta( days = -30 )
    date_from = getFormatDate( date = date_before_30days,format = "%Y-%m-%d" )
    date_to = getFormatDate( date = now ,format = "%Y-%m-%d")

    # 从‘全站日统计表’查询近30日的数据，得到一个列表
    list = StatDailySite.query.filter(  StatDailySite.date >= date_from)\
        .filter( StatDailySite.date <= date_to ).order_by( StatDailySite.id.asc() )\
        .all()
    data = resp_data['data']

    if list:
        for item in list:
            data['finance']['month'] += item.total_pay_money           # 当日应收总金额进行累加
            data['member']['month_new'] += item.total_new_member_count # 当日新增会员数进行累加
            data['member']['total'] = item.total_member_count           # 会员总数
            data['order']['month'] += item.total_order_count            # 当日订单数进行累加
            data['shared']['month'] += item.total_shared_count          # 当日分享数进行累加
            if getFormatDate( date = item.date ,format = "%Y-%m-%d") == date_to:
                data['finance']['today'] = item.total_pay_money    # 当日应收总金额
                data['member']['today_new'] = item.total_new_member_count   # 当日新增会员数
                data['order']['today'] = item.total_order_count  # 当日订单数
                data['shared']['today'] = item.total_shared_count  # 当日分享数

    return ops_render( "index/index.html",resp_data )