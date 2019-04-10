
from application import app,manager
from flask_script import Server
import www


# 自定义命令web server
manager.add_command("runserver",Server(host=app.config['SERVER_HOST'],port=app.config['SERVER_PORT'],use_debugger=True,use_reloader=True))

def main():
    # 运行程序
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        # 打印错误信息
        traceback.print_exc()






