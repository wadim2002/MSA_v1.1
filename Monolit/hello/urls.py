from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.wellcome),    
    #path('well', views.index),
    # login
    path("login/<str:name>/<str:password>", views.login),
    # user/register
    path("user/register/<str:name>/<str:surname>/<int:old>/<str:sex>/<str:hobby>/<str:sity>/<str:password>", views.register),
    # user/get/{id}
    path("user/get/<int:id>", views.getuser),
    # /user/search
    path("user/search/<str:firstName>/<str:secondName>", views.search),
    # Реализовать функционал поиска анкет по префиксу имени и фамилии (одновременно) в вашей социальной сети (реализовать метод /user/search из спецификации)
    # (запрос в форме firstName LIKE ? and secondName LIKE ?). Сортировать вывод по id анкеты. Использовать InnoDB движок.
    #path("user/post/feed", views.getpost2),
    #Реализовать функционал:
    ##(опционально) Добавление/удаление друга (методы /friend/add, /friend/delete из спецификации)
    #(опционально) CRUD для постов пользователей (методы /post/create, /post/update, /post/delete, /post/get из спецификации)
    #Лента постов друзей (метод /post/feed
    path("user/post/feed", views.getposts),
    path("user/post/refresh", views.refresh),
    path("user/post/create", views.refresh),

    #Отправка сообщения пользователю (метод /dialog/{user_id}/send из спецификации)
    path("dialog/<int:user>/send/<str:text>", views.dialog_send),
    #Получение диалога между двумя пользователями (метод /dialog/{user_id}/list из спецификации)
    #отправка сообщений в канал /post/feed/posted
    path("post/feed/posted", views.post_send),

    #чтение сообщения из канала
    path("post/feed/read", views.post_read),


    # Создать пост (Legacy)
    path("user/post/v1/create/<int:userid>/<str:text>", views.post_create),
    # Прочитать пост (Legacy)
    path("user/post/v1/read/<int:id>", views.post_read),

    # Создать пост (MSA)
    path("user/post/v2/create/<int:userid>/<str:text>", views.post_createmq),
    # Прочитать пост (MSA)
    path("user/post/v2/read/<int:id>", views.post_readmq),
    # Получить количество НЕпрочитанных постов
    path("user/post/noread", views.post_noread),
]
