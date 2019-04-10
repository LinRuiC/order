# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.schema import FetchedValue
from application import db


class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 美食名称
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    # 售卖金额
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    # 主图
    main_image = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    # 描述
    summary = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue())
    # 库存量
    stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # tag关键字，以","连接
    tags = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    # 状态 1：有效 0：无效
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 月销售数量
    month_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 总销售量
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 总浏览次数
    view_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 总评论量
    comment_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 最后更新时间
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    # 最后插入时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
