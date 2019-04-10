
from application import app

# 统一拦截处理和统一错误处理
from web.interceptors.AuthInterceptor import *
from web.interceptors.ApiAuthInterceptor import  *
from web.interceptors.ErrorInterceptor import  *

from web.controllers.index import route_index
from web.controllers.user.User import route_user
from web.controllers.static import route_static
from web.controllers.account.Account import route_account
from web.controllers.food.Food import route_food
from web.controllers.member.Member import route_member
from web.controllers.finance.Finance import route_finance
from web.controllers.stat.Stat import route_stat
from web.controllers.api import route_api
from web.controllers.upload.Upload import route_upload
from web.controllers.chart import route_chart

# 注册蓝图
app.register_blueprint(route_index,url_prefix="/")
# 用户蓝图
app.register_blueprint(route_user,url_prefix="/user")
# 静态资源查找路径蓝图
app.register_blueprint(route_static,url_prefix="/static")
# 账号管理
app.register_blueprint(route_account,url_prefix="/account")
# 美食管理
app.register_blueprint(route_food,url_prefix="/food")
# 会员管理
app.register_blueprint(route_member,url_prefix="/member")
# 财务管理
app.register_blueprint(route_finance,url_prefix="/finance")
# 统计管理
app.register_blueprint(route_stat,url_prefix="/stat")
# 小程序api入口管理
app.register_blueprint(route_api,url_prefix="/api")
# 图片上传
app.register_blueprint( route_upload,url_prefix = "/upload" )
# 财务管理
app.register_blueprint( route_chart,url_prefix = "/chart" )

