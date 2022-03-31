from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index/')
def index():
    db_session.global_init(f"db/mars_explorer.sqlite")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    jobs_count = len(jobs)
    return render_template("jobs_list.html",
                           title="Журнал работ",
                           jobs=jobs,
                           jobs_count=jobs_count)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="There is already such a user")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


def main():
    db_session.global_init('db/mars_explorer.sqlite')
    app.run()


if __name__ == '__main__':
    main()
