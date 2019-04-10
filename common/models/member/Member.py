# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db,app


class Member(db.Model):
    '''会员表'''
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    # 会员名
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    # 会员手机号码
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    # 性别 1：男 2：女
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 会员头像
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    # 随机salt
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    # 注册ip
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    # 状态 1：有效 0：无效
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 最后一 次更新时间
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    # 插入时 间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][ str( self.status ) ]

    @property
    def sex_desc(self):
        sex_mapping = {
            "0":"未知",
            "1":"男",
            "2":"女"
        }
        return sex_mapping[str(self.sex)]