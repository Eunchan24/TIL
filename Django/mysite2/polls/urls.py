from django.urls import path
from polls import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),                                # /polls/
    path('<int:question_id>/', views.detail, name='detail'),            # /polls/넘버/
    path('<int:question_id>/results/', views.results, name='results'),  # /polls/넘버/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),           # /polls/넘버/vote/
]
