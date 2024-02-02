from django.urls import path, include
from . import views
urlpatterns = [
    # Страница приветствия
    path('', views.wellcome),
    # Создать пост 
    path("user/post/create/<int:userid>/<str:text>", views.post_create),
    # Прочитать пост
    path("user/post/read/<int:id>", views.post_read),
    
    # Получить посты через очередь
    path("user/post/readmq", views.post_readmq),

    # Отправить пост через очередь
    path("user/post/writemq/<str:text>", views.post_writemq),

]