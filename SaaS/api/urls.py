from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from .views.auth import *
from .views.curator import *
from .views.student import *
from .views.theme import *
from .views.work import *
from .views.skill import *


urlpatterns = [
    # docs
    path('', get_swagger_view(title="MobileLab-Backend API")),
    # login branch
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    # curator branch
    path('curators', CuratorList.as_view()),
    path('curators/<int:curator_id>', CuratorDetail.as_view()),
    path('curators/<int:curator_id>/skills', CuratorSkillList.as_view()),
    path('curators/<int:curator_id>/works', CuratorWorkList.as_view()),
    path('curators/<int:curator_id>/works/<int:work_id>', CuratorWorkDetail.as_view()),
    path('curators/<int:curator_id>/works/<int:work_id>/steps', CuratorWorkStepList.as_view()),
    path('curators/<int:curator_id>/works/<int:work_id>/steps/<int:step_id>', CuratorWorkStepDetail.as_view()),
    path('curators/<int:curator_id>/works/<int:work_id>/steps/<int:step_id>/materials', CuratorWorkStepMaterialList.as_view()),
    path('curators/<int:curator_id>/works/<int:work_id>/steps/<int:step_id>/comments', CuratorWorkStepCommentList.as_view()),
    path('curators/<int:curator_id>/themes', CuratorThemeList.as_view()),
    path('curators/<int:curator_id>/themes/<int:theme_id>', CuratorThemeDetail.as_view()),
    path('curators/<int:curator_id>/suggestions', CuratorSuggestionList.as_view()),
    path('curators/<int:curator_id>/suggestions/<int:suggestion_id>', CuratorSuggestionDetail.as_view()),
    path('curators/<int:curator_id>/suggestions/<int:suggestion_id>/comments', CuratorSuggestionCommentList.as_view()),
    # student branch
    path('students', StudentList.as_view()),
    path('students/<int:student_id>', StudentDetail.as_view()),
    path('students/<int:student_id>/skills', StudentSkillList.as_view()),
    path('students/<int:student_id>/works', StudentWorkList.as_view()),
    path('students/<int:student_id>/works/<int:work_id>', StudentWorkDetail.as_view()),
    path('students/<int:student_id>/works/<int:work_id>/steps', StudentWorkStepList.as_view()),
    path('students/<int:student_id>/works/<int:work_id>/steps/<int:step_id>', StudentWorkStepDetail.as_view()),
    path('students/<int:student_id>/works/<int:work_id>/steps/<int:step_id>/materials', StudentWorkStepMaterialList.as_view()),
    path('students/<int:student_id>/works/<int:work_id>/steps/<int:step_id>/comments', StudentWorkStepCommentList.as_view()),
    path('students/<int:student_id>/themes', StudentThemeList.as_view()),
    path('students/<int:student_id>/themes/<int:theme_id>', StudentThemeDetail.as_view()),
    path('students/<int:student_id>/suggestions', StudentSuggestionList.as_view()),
    path('students/<int:student_id>/suggestions/<int:suggestion_id>', StudentSuggestionDetail.as_view()),
    path('students/<int:student_id>/suggestions/<int:suggestion_id>/comments', StudentSuggestionCommentList.as_view()),
    # themes branch
    path('themes', ThemeList.as_view()),
    path('themes/<int:theme_id>', ThemeDetail.as_view()),
    path('themes/<int:theme_id>/skills', ThemeSkillList.as_view()),
    # theme subject branch
    path('subjects', SubjectList.as_view()),
    path('subjects/<int:subject_id>', SubjectDetail.as_view()),
    # works branch
    path('works', WorkList.as_view()),
    path('works/<int:work_id>', WorkDetail.as_view()),
    path('works/<int:work_id>/steps', WorkStepList.as_view()),
    path('works/<int:work_id>/steps/<int:step_id>', WorkStepDetail.as_view()),
    path('works/<int:work_id>/steps/<int:step_id>/materials', WorkStepMaterialList.as_view()),
    # skills branch
    path('skills', SkillList.as_view()),
    path('skills/<int:skill_id>', SkillDetail.as_view())
]
