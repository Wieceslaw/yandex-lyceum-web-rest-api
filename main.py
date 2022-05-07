from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import LoginForm, JobForm, DepartmentForm
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data import jobs_api
from data import users_api
from requests import get
from find import get_image
from flask_restful import abort, Api
from data import users_resources
from data import jobs_resources


app = Flask(__name__)
api = Api(app)

# для списка объектов
api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')

# для одного объекта
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:users_id>')
api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/users_show/<int:user_id>', methods=['GET'])
def user_show(user_id):
    user = get(f'http://127.0.0.1:8080/api/users/{user_id}').json()['users']
    map_file = "static/img/map.png"
    get_image(user["city_from"], map_file)
    return render_template('users_show.html',
                           name=user['name'],
                           surname=user['surname'],
                           city_from=user['city_from'],
                           title='Hometown')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user.email == form.email.data and user.hashed_password == form.password.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect username or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/departments')
def list_of_departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department)
    return render_template("departments.html", title='List of Departments', departments=departments)


@app.route('/department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect("/departments")
    return render_template('department.html', title='Adding a Department', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).filter(Department.id == id,
                                                   ((Department.user == current_user) | (current_user.id == 1))
                                                   ).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(Department.id == id,
                                                       ((Department.user == current_user) | (current_user.id == 1))
                                                       ).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(Department.id == id,
                                                       ((Department.user == current_user) | (current_user.id == 1))
                                                       ).first()
        if departments:
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html', title='Еditing a Department', form=form)


@app.route('/job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('job.html', title='Adding a job', form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Еditing a job', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.user == current_user) | (current_user.id == 1))).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("jobs.html", title='Work log', jobs=jobs)


def main():
    db_session.global_init("db/astro.db")
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()