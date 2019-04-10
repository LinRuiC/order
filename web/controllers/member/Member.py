from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate,getDictFilterField,selectFilterObj
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from common.models.member.MemberComments import MemberComments
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from application import app,db

route_member = Blueprint( 'member_page',__name__ )

# 会员管理首页
@route_member.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    print("req--------------------",req)
    # 第几页 页数 没有传递默认为1
    page  = int( req['p'] ) if ( 'p' in req and req['p'] ) else 1
    query = Member.query

    # 按姓名或者手机号码查询
    if 'mix_kw' in req:
        query = query.filter( Member.nickname.ilike( "%{0}%".format( req['mix_kw'] ) ) )

    # 按状态查询 正常或已删除或者默认 int(-1)=-1
    if 'status' in req and int( req['status'] ) > -1 :
        query = query.filter( Member.status == int( req['status'] ) )

    page_params = {
        'total':query.count(),  # 查询到的数据条数
        'page_size': app.config['PAGE_SIZE'], # 每页显示的数据条数
        'page':page,    # 第几页
        'display':app.config['PAGE_DISPLAY'], # 显示几个分页
        'url': request.full_path.replace("&p={}".format(page),"") # 构建url参数
    }

    pages = iPagination( page_params )
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    list = query.order_by( Member.id.desc() ).offset( offset ).limit( app.config['PAGE_SIZE'] ).all()

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render( "member/index.html",resp_data )

# 会员信息
@route_member.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    # 获取前端传递过来的会员id  没有默认为0
    id = int( req.get( "id",0 ) )
    reback_url = UrlManager.buildUrl( "/member/index" )
    if id < 1:
        return redirect( reback_url )

    # 按会员id从会员表获取会员信息
    info = Member.query.filter_by( id =id ).first()
    if not info:
        return redirect( reback_url )

    # status（1：支付完成 0 无效 -1 申请退款 -2 退款中 -9 退款成功  -8 待支付  -7 完成支付待确认）
    # 从“在线购买订单表”查询该会员状态不为退款成功的所有订单
    pay_order_list = PayOrder.query.filter_by( member_id = id ).filter( PayOrder.status.in_( [-8,1] ) )\
        .order_by( PayOrder.id.desc() ).all()
    # 从“会员评论表”查询该会员所有的评论
    comment_list = MemberComments.query.filter_by( member_id = id ).order_by( MemberComments.id.desc() ).all()

    resp_data['info'] = info # 会员信息
    resp_data['pay_order_list'] = pay_order_list # 会员的所有订单
    resp_data['comment_list'] = comment_list #该会员的评论信息
    resp_data['current'] = 'index' # 状态栏
    return ops_render( "member/info.html",resp_data )

# 会员信息设置保存
@route_member.route( "/set",methods = [ "GET","POST" ] )
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int( req.get( "id",0 ) )
        reback_url = UrlManager.buildUrl("/member/index")
        if id < 1:
            return redirect(reback_url)

        info = Member.query.filter_by(id=id).first()
        if not info:
            return redirect(reback_url)

        if info.status != 1:
            return redirect(reback_url)

        resp_data['info'] = info
        resp_data['current'] = 'index'
        return ops_render( "member/set.html",resp_data )

    resp = { 'code':200,'msg':'操作成功~~','data':{} }
    req = request.values
    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify( resp )

    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在~~"
        return jsonify(resp)

    member_info.nickname = nickname
    member_info.updated_time = getCurrentDate()
    db.session.add( member_info )
    db.session.commit()
    return jsonify( resp )

# 会员评论
@route_member.route( "/comment" )
def comment():
    resp_data = {}
    req = request.args
    # 获取前端传递过来的会员id  没有默认为1
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = MemberComments.query

    page_params = {
        'total': query.count(), # 所有的评论数据条数
        'page_size': app.config['PAGE_SIZE'],  # 每页显示的数据条数
        'page': page,   # 第几页
        'display': app.config['PAGE_DISPLAY'], # 显示几个分页
        'url': request.full_path.replace("&p={}".format(page), "")   # 构建url参数
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    # 该页面要显示的评论数据
    comment_list = query.order_by(MemberComments.id.desc()).offset( offset ).limit( app.config['PAGE_SIZE'] ).all()
    data_list = []
    if comment_list:
        # getDictFilterField()根据某个字段获取一个dic出来 从数据库获取指定条件的数据
        member_map = getDictFilterField( Member,Member.id,"id", selectFilterObj( comment_list ,"member_id" ) )
        food_ids = []
        for item in comment_list:
            tmp_food_ids = (item.food_ids[1:-1]).split("_")
            tmp_food_ids = {}.fromkeys( tmp_food_ids ).keys()
            food_ids = food_ids + list( tmp_food_ids )

        food_map = getDictFilterField( Food,Food.id,"id", food_ids )

        for item in comment_list:
            tmp_member_info = member_map[ item.member_id ]
            tmp_foods = []
            tmp_food_ids = (item.food_ids[1:-1]).split("_")
            for tmp_food_id in tmp_food_ids:
                tmp_food_info = food_map[ int( tmp_food_id ) ]
                tmp_foods.append({
                    'name': tmp_food_info.name,
                })

            tmp_data = {
                "content":item.content,
                "score":item.score,
                "member_info":tmp_member_info,
                "foods":tmp_foods
            }
            data_list.append( tmp_data )
    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['current'] = 'comment'

    return ops_render( "member/comment.html",resp_data )

# 询问是否确定 删除/回复 弹框
@route_member.route("/ops",methods=["POST"])
def ops():
    resp = { 'code':200,'msg':'操作成功~~','data':{} }
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id :
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in [ 'remove','recover' ]:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    member_info = Member.query.filter_by( id = id ).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在~~"
        return jsonify(resp)

    if act == "remove":
        member_info.status = 0
    elif act == "recover":
        member_info.status = 1

    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()
    return jsonify( resp )
