"""
Util for filling database with test data
"""

import os

from django.db.models.manager import Manager
from django.contrib.auth.models import Group, User

from .csv import csv_entry_list_reader
from ....models.curator import Curator
from ....models.student import Student
from ....models.student import Group as AcademicGroup
from ....models.skill import Skill
from ....models.theme import Subject, Theme
from ....models.work import Work, WorkStep, WorkStepStatus, WorkStepMaterial, WorkStepComment
from ....models.suggestion import SuggestionTheme, SuggestionThemeStatus

import random
from datetime import timedelta
from ...datetime_converter import str2dt

date_field_name = ['date_creation', 'date_acceptance', 'date_start', 'date_finish']


def migrate_to_db_user(manager_model: Manager,
                       manager_user: Manager,
                       group: Group,
                       csv_file_path: str):
    path = os.path.abspath(csv_file_path)
    with open(path, encoding='utf8') as file:
        _list = csv_entry_list_reader(file)

    manager_model.all().delete()
    print("All models(Manager: {}) deleted.".format(manager_model))
    for entry in _list:
        for date_field in date_field_name:
            if entry.get(date_field, None):
                entry[date_field] = str2dt(entry[date_field])
            else:
                entry.pop(date_field, None)

        first_name = entry['name']
        last_name = entry['last_name']
        patronymic = entry['patronymic']
        username = "{0}.{1}.{2}".format(first_name, last_name, patronymic)
        password = username
        user = manager_user.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.groups.add(group)
        user.save()

        model = manager_model.create(credentials=user, **entry)
        model.credentials = user
        model.save()

        print("User: {0}. Model: {1}.".format(user, model))


def migrate_to_db(manager: Manager, csv_file_path: str, manager_related: Manager = None,
                  related_field_name: str = None, related_model_field_name: str = None):
    path = os.path.abspath(csv_file_path)
    with open(path, encoding='utf8') as file:
        _list = csv_entry_list_reader(file)

    manager.all().delete()
    print("All models(Manager: {}) deleted.".format(manager))

    related_list = None
    if manager_related:
        related_list = list(manager_related.all())

    for entry in _list:
        for date_field in date_field_name:
            if entry.get(date_field, None):
                entry[date_field] = str2dt(entry[date_field])
            else:
                entry.pop(date_field, None)

        if related_list and related_field_name and related_model_field_name:
            entry[related_field_name] = getattr(random.choice(related_list), related_model_field_name)

        _object = manager.create(**entry)
        print(_object)


def link_related_to_man(men: list, skills: list, groups: list = None):
    for man in men:
        count = random.randint(1, 10)
        for i in range(count):
            skill = random.choice(skills)
            man.skills.add(skill)
            print("{} -> {}".format(str(skill), str(man)))

            if groups:
                group = random.choice(groups)
                man.group = group
                print("{} -> {}".format(str(group), str(man)))
            man.save()


def init_line_theme():
    curator = Curator.objects.first()
    student = Student.objects.first()
    subject = Subject.objects.get(name__startswith="Робот")
    skills = [
        Skill.objects.get(name__exact="Cpp"),
        Skill.objects.get(name__exact="Python"),
    ]
    theme = Theme.objects.get(title__startswith="Антропоморфный")
    theme.curator = curator
    theme.student = student
    theme.subject = subject
    for skill in skills:
        theme.skills.add(skill)
    theme.save()

    work = Work.objects.create(theme=theme, date_start=theme.date_creation,
                               date_finish=theme.date_creation + timedelta(days=30))
    work_step_status = WorkStepStatus.objects.get(name__exact="Выполнен")
    work_steps = [
        WorkStep.objects.create(title="Написание плана", description="План на время работы",
                                date_start=str2dt("2018-05-09T19:17:25.473086Z"),
                                date_finish=str2dt("2018-05-10T18:17:25.473086Z"),
                                work=work, status=work_step_status),
        WorkStep.objects.create(title="Ознакомление с литературой", description="Чтение литературы из книги",
                                date_start=str2dt("2018-05-10T18:17:25.473086Z"),
                                date_finish=str2dt("2018-05-17T18:17:25.473086Z"),
                                work=work, status=work_step_status),
        WorkStep.objects.create(title="Проежуточный отчёт", description="Отчёт о проделанной работе",
                                date_start=str2dt("2018-05-29T09:17:25.473086Z"),
                                date_finish=str2dt("2018-05-29T13:17:25.473086Z"),
                                work=work, status=work_step_status),
        WorkStep.objects.create(title="Сдать работу", description="Сдача",
                                date_start=str2dt("2018-06-08T10:10:25.473086Z"),
                                date_finish=str2dt("2018-06-08T15:10:25.473086Z"),
                                work=work, status=work_step_status)
    ]
    materials_content = ["http://google.com/", "http://cppreference.com/", "http://wiki.ros.com/"]
    for step in work_steps:
        WorkStepComment.objects.create(author_name=curator.name, content="приложил материал",
                                       date_creation=str2dt("2018-05-10T19:17:25.473086Z"),
                                       step=step)
        WorkStepMaterial.objects.create(content=random.choice(materials_content), step=step)


def init_line_theme_suggestion():
    SuggestionTheme.objects.all().delete()
    curator = Curator.objects.last()
    student = Student.objects.last()
    subject = Subject.objects.get(name__exact="Разработка веб-приложений")
    skills = [
        Skill.objects.get(name__exact="HTML"),
        Skill.objects.get(name__exact="CSS"),
        Skill.objects.get(name__exact="Javascript"),
    ]
    theme = Theme.objects.get(title__startswith="Kahoot")
    theme.curator = curator
    theme.student = student
    theme.subject = subject
    for skill in skills:
        theme.skills.add(skill)

    suggestion = SuggestionTheme.objects.create(theme=theme, student=student, curator=curator,
                                                status=SuggestionThemeStatus.objects.get(name__exact="Нет ответа"),
                                                date_creation=theme.date_creation)


def do():
    path = './SaaS/api/mylog/db/test-data'
    migrate_to_db(Skill.objects, path + '/skill.csv')

    User.objects.all().delete()
    print("All users(Manager: {}) deleted.".format(User.objects))
    migrate_to_db_user(Curator.objects, User.objects, Group.objects.get(name="curators"), path + '/curator.csv')
    migrate_to_db_user(Student.objects, User.objects, Group.objects.get(name="students"), path + '/student.csv')

    migrate_to_db(AcademicGroup.objects, path + '/group.csv')
    migrate_to_db(WorkStepStatus.objects, path + '/work_step_status.csv')
    migrate_to_db(SuggestionThemeStatus.objects, path + '/suggestion_theme_status.csv')
    migrate_to_db(Subject.objects, path + '/subject.csv')
    migrate_to_db(Theme.objects, path + '/theme.csv', Subject.objects, "subject_id", "id")

    skills = list(Skill.objects.all())
    academic_groups = list(AcademicGroup.objects.all())
    link_related_to_man(list(Curator.objects.all()), skills)
    link_related_to_man(list(Student.objects.all()), skills, academic_groups)
    init_line_theme()
    init_line_theme_suggestion()
