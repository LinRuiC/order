# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class MemberComments(db.Model):
    # 会员评论表
    __tablename__ = 'member_comments'

    id = db.Column(db.Integer, primary_key=True)
    # 会员id
    member_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    # 商品ids
    food_ids = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    # 订单id
    pay_order_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 评分
    score = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 评论内容
    content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    # 插入时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def score_desc(self):
        score_map = {
            "10": "好评",
            "6": "中评",
            "0": "差评",
        }
        return score_map[ str( self.score ) ]
