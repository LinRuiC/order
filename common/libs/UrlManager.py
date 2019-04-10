# -*- coding: utf-8 -*-
import time
from application import  app


class UrlManager(object):
    def __init__(self):
        pass

    # 构建url路径
    @staticmethod
    def buildUrl( path ):
        return path

    # 构建静态文件路径
    @staticmethod
    def buildStaticUrl(path):
        # 更新静态js,html等文件版本号 免去手动更新的操作 RELEASE_VERSION改变就会更新网页缓存
        release_version = app.config.get( 'RELEASE_VERSION' )
        ver = "%s"%( int( time.time() ) ) if not release_version else release_version
        path =  "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl( path )

    # 构建图片路径
    @staticmethod
    def buildImageUrl( path ):
        app_config = app.config['APP']
        url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url