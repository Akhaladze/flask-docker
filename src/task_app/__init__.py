from celery import Celery
from celery import Task
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
            max_tasks_per_child=1,
            max_workers_per_child=1,
            worker_prefetch_multiplier=1,
            worker_max_tasks_per_child=1,
            task_routes={
                "task_app.getShellyStatuses": "low-priority",
                "task_app.tasks.add": "low-priority",
                "task_app.tasks.block": "low-priority",
                "task_app.tasks.process": "low-priority",
            },
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    @app.route("/getShellyStatuses")
    def getShellyStatuses() -> str:
        return render_template("getshellystatuses.html")
        
    from . import views

    app.register_blueprint(views.bp)
    return app

    
        

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app