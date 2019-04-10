# 这里的配置是所有模式共用的

# 启动IP地址，端口
SERVER_HOST='127.0.0.1'
SERVER_PORT=5000

DEBUG=True

# mysql数据库配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/food_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 打印所有SQL语句
SQLALCHEMY_ECHO=True
SQLALCHEMY_ENCODING='utf-8'

# 设置的cookie名称
AUTH_COOKIE_NAME = "mooc_food"

SEO_TITLE = "Python Flask构建微信小程序订餐系统"

##过滤url 就是不用验证是否登录
IGNORE_URLS = [
    "^/user/login"
]

# 小程序
API_IGNORE_URLS = [
    "^/api"
]

# 不用验证是否登录
IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

# 每页显示的最多数据条数
PAGE_SIZE = 10
# 显示几个分页
PAGE_DISPLAY = 10

# 状态查询
STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}

# 静态文件要添加的版本号
RELEASE_VERSION="20190326"

# 小程序配置
MINA_APP = {
    'appid':'wxee88743aa7d6829a', # 小程序id
    'appkey': '9a3486fdd0e7db7e71f27ef6b9912fdd',
    'paykey':'', #商户支付密钥
    'mch_id':'',  # 商户号
    'callback_url':'/api/order/callback'
}

# 上传图片设置
UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/'
}

# 项目运行的绝对路径
APP = {
    'domain':'http://127.0.0.1:5000'
}


PAY_STATUS_MAPPING = {
    "1":"已支付",
    "-8":"待支付",
    "0":"已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}




