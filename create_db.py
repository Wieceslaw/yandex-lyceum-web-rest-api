from data import db_session
import datetime
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.category import Category


def main():
    db_session.global_init("db/astro.db")
    capitan = User()
    capitan.surname = "Scott"
    capitan.name = "Ridley"
    capitan.age = 21
    capitan.position = "captain"
    capitan.speciality = "research engineer"
    capitan.address = "module_1"
    capitan.email = "scott_chief@mars.org"
    capitan.set_password('password')
    capitan.city_from = 'Berlin'

    colon1 = User()
    colon1.surname = "Weir"
    colon1.name = "Andy"
    colon1.age = 18
    colon1.position = "common"
    colon1.speciality = "worker"
    colon1.address = "module_1"
    colon1.email = "colon1@mars.org"
    colon1.city_from = 'New York'

    colon2 = User()
    colon2.surname = "Sanders"
    colon2.name = "Teddy"
    colon2.age = 19
    colon2.position = "common"
    colon2.speciality = "worker"
    colon2.address = "module_2"
    colon2.email = "colon2@mars.org"
    colon2.city_from = 'Paris'

    category1 = Category()
    category1.name = '1'

    category2 = Category()
    category2.name = '2'

    category3 = Category()
    category3.name = '3'

    job1 = Jobs()
    job1.team_leader = 1
    job1.job = "deployment of residential modules 1 and 2"
    job1.work_size = 15
    job1.collaborators = "2, 3"
    job1.start_date = datetime.datetime.now()
    job1.is_finished = False
    job1.categories.append(category1)

    job2 = Jobs()
    job2.team_leader = 2
    job2.job = "Exploration of mineral resourses"
    job2.work_size = 15
    job2.collaborators = "4, 3"
    job2.start_date = datetime.datetime.now()
    job2.is_finished = False
    job2.categories.append(category2)

    job3 = Jobs()
    job3.team_leader = 3
    job3.job = "Development of management system"
    job3.work_size = 25
    job3.collaborators = "5"
    job3.start_date = datetime.datetime.now()
    job3.is_finished = True
    job3.categories.append(category3)

    department1 = Department()
    department1.title = 'Department of geological exploration'
    department1.chief = 2
    department1.members = '1, 2, 3'
    department1.email = 'geo@mars.org'

    department2 = Department()
    department2.title = 'Department of biological research'
    department2.chief = 3
    department2.members = '2, 3'
    department2.email = 'bio@mars.org'

    department3 = Department()
    department3.title = 'Department of construction'
    department3.chief = 1
    department3.members = '1, 3'
    department3.email = 'build@mars.org'

    db_sess = db_session.create_session()
    db_sess.add(capitan)
    db_sess.add(colon1)
    db_sess.add(colon2)
    db_sess.add(job1)
    db_sess.add(job2)
    db_sess.add(job3)
    db_sess.add(department1)
    db_sess.add(department2)
    db_sess.add(department3)
    db_sess.add(category1)
    db_sess.add(category2)
    db_sess.add(category3)
    db_sess.commit()


if __name__ == '__main__':
    main()