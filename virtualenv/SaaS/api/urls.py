from django.urls import path

from . import views


urlpatterns = [
    # curator branch
    path('curators', views.CuratorList.as_view()),
    path('curators/<int:pk>', views.CuratorDetail.as_view()),
    path('curators/<int:pk>/skills', views.CuratorSkillList.as_view()),
    path('curators/<int:pk>/works', views.CuratorWorkList.as_view()),
    path('curators/<int:pk>/works/<int:pk>', views.CuratorWorkDetail.as_view()),
    path('curators/<int:pk>/works/<int:pk>/steps', views.CuratorWorkStepList.as_view()),
    path('curators/<int:pk>/works/<int:pk>/steps/<int:pk>', views.CuratorWorkStepDetail.as_view()),
    path('curators/<int:pk>/works/<int:pk>/steps/<int:pk>/materials', views.CuratorWorkStepMaterialList.as_view()),
    path('curators/<int:pk>/works/<int:pk>/steps/<int:pk>/comments', views.CuratorWorkStepCommentList.as_view()),
    path('curators/<int:pk>/themes', views.CuratorThemeList.as_view()),
    path('curators/<int:pk>/themes/<int:pk>', views.CuratorThemeDetail.as_view()),
    path('curators/<int:pk>/suggestions', views.CuratorSuggestionList.as_view()),
    path('curators/<int:pk>/suggestions/<int:pk>', views.CuratorSuggestionDetail.as_view()),
    path('curators/<int:pk>/suggestions/<int:pk>/comments', views.CuratorSuggestionCommentList.as_view()),
    # student branch
    path('students', views.StudentList.as_view()),
    path('students/<int:pk>', views.StudentDetail.as_view()),
    path('students/<int:pk>/skills', views.StudentSkillList.as_view()),
    path('students/<int:pk>/works', views.StudentWorkList.as_view()),
    path('students/<int:pk>/works/<int:pk>', views.StudentWorkDetail.as_view()),
    path('students/<int:pk>/works/<int:pk>/steps', views.StudentWorkStepList.as_view()),
    path('students/<int:pk>/works/<int:pk>/steps/<int:pk>', views.StudentWorkStepDetail.as_view()),
    path('students/<int:pk>/works/<int:pk>/steps/<int:pk>/materials', views.StudentWorkStepMaterialList.as_view()),
    path('students/<int:pk>/works/<int:pk>/steps/<int:pk>/comments', views.StudentWorkStepCommentList.as_view()),
    path('students/<int:pk>/themes', views.StudentThemeList.as_view()),
    path('students/<int:pk>/themes/<int:pk>', views.StudentThemeDetail.as_view()),
    path('students/<int:pk>/suggestions', views.StudentSuggestionList.as_view()),
    path('students/<int:pk>/suggestions/<int:pk>', views.StudentSuggestionDetail.as_view()),
    path('students/<int:pk>/suggestions/<int:pk>/comments', views.StudentSuggestionCommentList.as_view()),
    # themes branch
    path('themes', views.ThemeList.as_view()),
    path('themes/<int:pk>', views.ThemeDetail.as_view()),
    path('themes/<int:pk>/skills', views.ThemeSkillList.as_view()),
    # works branch
    path('works', views.WorkList.as_view()),
    path('works/<int:pk>', views.WorkDetail.as_view()),
    path('works/<int:pk>/steps', views.WorkStepList.as_view()),
    path('works/<int:pk>/steps/<int:pk>', views.WorkStepDetail.as_view()),
    path('works/<int:pk>/steps/<int:pk>/materials', views.WorkStepMaterialList.as_view()),
]