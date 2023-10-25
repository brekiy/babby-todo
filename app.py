import datetime
import flask

import models

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
def home():
    task_list = models.task.Task.query.all()
    tasks_processed = {
        "complete": {},
        "incomplete": {}
    }

    for task in task_list:
        completion = "complete" if task.completed else "incomplete"
        category = task.category if task.category is not None else "Uncategorized"

        if category not in tasks_processed[completion]:
            tasks_processed[completion][category] = []
        tasks_processed[completion][category].append(task)
        print(tasks_processed)
    return flask.render_template("home.html", tasks=tasks_processed)

@app.route("/tasks/add", methods=["POST"])
def add_task():
    category = flask.request.form.get("category")
    name = flask.request.form.get("name")
    description = flask.request.form.get("description")
    goal_date = flask.request.form.get("date")
    if goal_date:
        goal_date = datetime.datetime.strptime(goal_date)
    new_task = models.task.Task(category=category, name=name, description=description, goal_date=goal_date,completed=False)
    models.db.session.add(new_task)
    models.db.session.commit()
    return flask.redirect(flask.url_for("home"))

@app.route("/tasks/complete/<task_id>", methods=["GET"])
def complete_task(task_id):
    task = models.task.Task.query.filter_by(id=task_id).first()
    task.completed = True
    models.db.session.commit()
    return flask.redirect(flask.url_for("home"))

@app.route("/tasks/delete/<task_id>", methods=["GET"])
def delete_task(task_id):
    task = models.task.Task.query.filter_by(id=task_id).first()
    models.db.session.delete(task)
    models.db.session.commit()
    return flask.redirect(flask.url_for("home"))


models.db.init_app(app)
with app.app_context():
    models.db.create_all()
app.run()