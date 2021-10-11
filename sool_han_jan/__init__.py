import os
from flask import Flask

# DB 파일 경로
DB_FILEPATH = os.path.join(os.getcwd(), 'data/Sools.db')
# CSV_FILEPATH = os.path.join(os.getcwd(), 'data/my_data.csv')

def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.update(config)

    # import & add blueprint
    from project_submit.views.main_views import main_bp
    from project_submit.views.user_views import user_bp

    app.register_blueprint(main_bp);
    app.register_blueprint(user_bp, url_prefix='/<name>/Sools');
    return app;

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True);

