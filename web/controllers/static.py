from flask import Blueprint,send_from_directory
from application import app


# HTML的静态资源路劲查找配置

route_static=Blueprint('static',__name__)
@route_static.route("/<path:filename>")
def index(filename):
    # 打印日志信息
    app.logger.info(filename)
    return send_from_directory(app.root_path+"/web/static/",filename)




