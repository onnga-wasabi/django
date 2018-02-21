from django.urls import path
from . import views

# 他にblogみたいなアプリを作った時にdetailとか同じ名前のviewを持ちたい時にスコープを定義し置くと便利っぽい
app_name = 'polls'
urlpatterns = [
    # /polls/
    path('', views.IndexView.as_view(), name='index'),
    # /polls/6/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # /polls/6/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # /polls/6/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
