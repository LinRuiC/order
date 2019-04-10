# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db,app


class FoodCat(db.Model):
    # 食品分类
    __tablename__ = 'food_cat'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    # 类别名称
    name = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    # 权重
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 状态 1：有效 0：无效
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 状态 1：有效 0：无效
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    # 插入时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    # 返回状态对应的字符串
    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][ str( self.status ) ]
