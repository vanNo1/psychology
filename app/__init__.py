from flask import Flask
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # 从config.py加载配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)

    # 确保上传目录存在
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)

    return app