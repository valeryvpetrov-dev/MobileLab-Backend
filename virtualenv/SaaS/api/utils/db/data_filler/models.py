"""
Util for filling database with test data
"""

import os

from django.db import models
from SaaS.api.models.curator import Curator
from SaaS.api.models.student import Student
from SaaS.api.models.skill import Skill
from SaaS.api.models.theme import Subject, Theme
from SaaS.api.models.work import Work, WorkStep, WorkStepStatus, WorkStepMaterial, WorkStepComment
from SaaS.api.models.suggestion import SuggestionTheme, SuggestionThemeStatus

from SaaS.api.utils.db.csv import *

import random
from datetime import timedelta
from SaaS.api.utils.datetime_converter import str2dt

date_field_name = ['date_creation', 'date_acceptance', 'date_start', 'date_finish']


def migrate_to_db(manager: models.manager.Manager, csv_file_path: str):
    path = os.path.abspath(csv_file_path)
    with open(path, encoding='utf8') as file:
        _list = csv_entry_list_reader(file)

    manager.all().delete()
    for entry in _list:
        for date_filed in date_field_name:
            if entry.get(date_filed, None):
                entry[date_filed] = str2dt(entry[date_filed])
            else:
                entry.pop(date_filed, None)

        _object = manager.create(**entry)
        print(_object)


def link_skills_to_man(list_skill: list, list_man: list):
    for man in list_man:
        count = random.randint(1, 10)
        for i in range(count):
            skill = random.choice(list_skill)
            man.skills.add(skill)
            print("{} -> {}".format(str(skill), str(man)))


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
    path = r'E:\Python\Django\MobileLab-Backend\mylog\db\test-data'
    migrate_to_db(Skill.objects, path + r'\skill.csv')
    migrate_to_db(Curator.objects, path + r'\curator.csv')
    migrate_to_db(Student.objects, path + r'\student.csv')
    migrate_to_db(Subject.objects, path + r'\subject.csv')
    migrate_to_db(Theme.objects, path + r'\theme.csv')
    migrate_to_db(WorkStepStatus.objects, path + r'\work_step_status.csv')
    migrate_to_db(SuggestionThemeStatus.objects, path + r'\suggestion_theme_status.csv')

    skills = list(Skill.objects.all())
    link_skills_to_man(skills, list(Curator.objects.all()))
    link_skills_to_man(skills, list(Student.objects.all()))
    init_line_theme()
    init_line_theme_suggestion()
