## Общие сведения
В проекте включены:
- Монолит
- БД монолита
- Сервис Постов
- БД сервиса
- Брокер

## Развертывание
docker-compose up

## Примеры работы
1) Чтение постов
http://localhost:8000/user/post/v1/read/1
http://localhost:8000/user/post/v2/read/2

2)  Создание постов
http://localhost:8000/user/post/v1/create/1/TextPostUser1
http://localhost:8000/user/post/v2/create/2/TextPostUser2

Задание:
 1. Описать протокол взаимодействия.
 Для функциональности Постов реализованы API
 # Создать пост (Legacy)
 "user/post/v1/create/<int:userid>/<str:text>"
 # Прочитать пост (Legacy)
 "user/post/v1/read/<int:id>"

 # Создать пост (MSA)
 "user/post/v2/create/<int:userid>/<str:text>"
 # Прочитать пост (MSA)
 "user/post/v2/read/<int:id>"

 2. Поддержание старых клиентов
 В состав проекта включен старый монолит с предыдущей версией API

 5. Организовать сквозное логирование запросов
    Реализована функция logger записывающая в файл logger.txt
    - Дату/Время
    - Название сервиса
    - Название операции