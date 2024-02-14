from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5tr6tyujkhnbvcfrty6u765432qwe6578iukjmnbvgtyyiuu7865esrdxfgcurt546uythjfdrezdfx'
    app.config['UPLOAD_FOLDER'] = 'static/files'

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app
