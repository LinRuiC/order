# -*- coding: utf-8 -*-
from flask import g,render_template
import datetime
'''
自定义分页类
'''
def iPagination( params ):
    import math

    ret = {
        "is_prev":1,    # 是否有上一页
        "is_next":1,    # 是否有下一页
        "from" :0 ,     # 起始的页数
        "end":0,        # 接收页数
        "current":0,    # 第几页
        "total_pages":0,## 总页数
        "page_size" : 0,# 每页最多显示数据条数
        "total" : 0,    # 总共的数据条数
        "url":params['url']
    }

    total = int( params['total'] )      # 按条件查询到的数据条数
    page_size = int( params['page_size'] ) # 每页最多显示的数据条数
    page = int( params['page'] )        # 第几页
    display = int( params['display'] )      # 显示几页
    total_pages = int( math.ceil( total / page_size ) ) # 计算出总共几页
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        # 页数第一页 没有上一页
        ret['is_prev'] = 0

    if page >= total_pages:
        # 页数为最后一页 没有下一页
        ret['is_next'] = 0

    # math.ceil为向上取整函数
    semi = int( math.ceil( display / 2 ) )

    if page - semi > 0 :
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages :
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page       # 第几页
    ret['total_pages'] = total_pages    # 总页数
    ret['page_size'] = page_size    # 每页最多显示数据条数
    ret['total'] = total    # 总共的数据条数
    ret['range'] = range( ret['from'],ret['end'] + 1 )
    return ret

'''
统一渲染方法
'''
def ops_render( template,context = {} ):
    if 'current_user' in g:
        context['current_user'] = g.current_user
    # template:跳转的url路径 context传递的上下文参数
    return render_template( template,**context )

'''
获取当前时间
'''
def getCurrentDate( format = "%Y-%m-%d %H:%M:%S"):
    #return datetime.datetime.now().strftime( format )
    return datetime.datetime.now()

'''
获取当前格式化的时间
'''
def getFormatDate( date = None ,format = "%Y-%m-%d %H:%M:%S" ):
    if date is None:
        date = datetime.datetime.now()

    return date.strftime( format )


'''
根据某个字段获取一个dict出来 从数据库获取指定条件的数据
'''
def getDictFilterField( db_model,select_filed,key_field,id_list ):
    '''
    :param db_model:  数据库
    '''
    ret = {}
    query = db_model.query
    if id_list and len( id_list ) > 0:
        query = query.filter( select_filed.in_( id_list ) )

    list = query.all()
    # 如果没有数据 返回空字典
    if not list:
        return ret
    for item in list:
    #     hasattr判断一个对象里面是否有key_field属性或者key_field方法，返回BOOL值，有name特性返回True， 否则返回False。
    #     需要注意的是key_field要用括号括起来
        if not hasattr( item,key_field ):
            break

        # getattr获取对象item的属性值或者方法的内存地址 这里是获取id属性的值和对象构成字典
        ret[ getattr( item,key_field ) ] = item
    return ret



def selectFilterObj( obj,field ):
    ret = []
    for item in obj:
        if not hasattr(item, field ):
            break
        if getattr( item,field )  in ret:
            continue
        ret.append( getattr( item,field ) )
    return ret


def getDictListFilterField( db_model,select_filed,key_field,id_list ):
    ret = {}
    query = db_model.query
    if id_list and len( id_list ) > 0:
        query = query.filter( select_filed.in_( id_list ) )

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr( item,key_field ):
            break
        if getattr( item,key_field ) not in ret:
            ret[getattr(item, key_field)] = []

        ret[ getattr( item,key_field ) ].append(item )
    return ret