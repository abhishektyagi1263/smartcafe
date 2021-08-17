from django.urls import path
from . import views

app_name = 'interface'

urlpatterns = [
    path('student/', views.test, name="student"),
    path('info/',views.info, name="info"),
    path('result/',views.result,name='result'),
    path('info/sub/',views.subcode),
    path('teacher/',views.teacher_view, name='teacher'),
    path('view_score/',views.submittion,name='view_score'),
    path('view_score/',views.submittion,name='view_score'),
    path('analysis/',views.analysis,name="analysis"),
    path('ques/',views.ques,name='ques'),
    path('statements/',views.stat,name='statements'),
    path('edit/<id>',views.edit_que),
    path('delete/<id>',views.deleteQue,name='del',),
    path('edit_all/',views.final),
    path('code/<int:id>',views.code),
    path('export/',views.export),
    path('ex/',views.ex),
    path('teacher_code/<int:id>',views.teacher_view_code_fun),
]
