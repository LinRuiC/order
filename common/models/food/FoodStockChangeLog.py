# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class FoodStockChangeLog(db.Model):
    # 数据库存变更表
    __tablename__ = 'food_stock_change_log'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, nullable=False, index=True)
    # 变更多少
    unit = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 变更之后总量
    total_stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 备注字段
    note = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    # 插入时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
