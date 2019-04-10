# -*- coding: utf-8 -*-
from application import app,db
from common.models.food.FoodStockChangeLog import FoodStockChangeLog
from common.models.food.Food import Food
from common.libs.Helper import getCurrentDate
class FoodService():

    @staticmethod
    def setStockChangeLog( food_id = 0,quantity = 0,note = '' ):

        if food_id < 1:
            return False

        food_info = Food.query.filter_by( id = food_id ).first()
        if not food_info:
            return False

        model_stock_change = FoodStockChangeLog()
        model_stock_change.food_id = food_id
        # 变更多少
        model_stock_change.unit = quantity
        # 变更之后总量
        model_stock_change.total_stock = food_info.stock
        # 备注字段
        model_stock_change.note = note
        # 修改时间
        model_stock_change.created_time = getCurrentDate()
        # 提交到数据库
        db.session.add(model_stock_change)
        db.session.commit()
        return True


