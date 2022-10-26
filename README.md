# minbox_DE
Тестовое задание на позицию Junior Data Engineer / MLOps
==============================
## Первая часть задания. 
Есть Pandas DataFrame со столбцами [“customer_id”, “product_id”, “timestamp”], который содержит данные по просмотрам товаров на сайте. Есть проблема – просмотры одного customer_id не разбиты на сессии (появления на сайте). Мы хотим разместить сессии так, чтобы сессией считались все смежные просмотры, между которыми не более 3 минут.

Написать методом который создаст в Pandas DataFrame столбец session_id и проставит в нем уникальный int id для каждой сессии.

У каждого пользователя может быть по несколько сессий. Исходный DataFrame может быть большим – до 100 млн строк.
Скрипт с решением лежит в src/task1.py

Запускается командой 
```commandline
python src/task1.py
```
## Вторая часть задания.
В SQL базе данных есть продукты и категории. Одному продукту может соответствовать много категорий, в одной категории может быть много продуктов.

Напишите HTTP API через которое можно получить:

список всех продуктов с их категориями,
список категорий с продуктами,
список всех пар «Имя продукта – Имя категории».
Если у продукта нет категорий, то он все равно должен выводиться.

Если у категории нет продуктов, то она все равно должна выводиться.

Проект должен содержать docker-compose.yml файл, через который можно запустить сервис и проверить его работу.

Контейнеры поднимаются командой 
```commandline
docker compose up 
```

При запуске контейнера автомотически добавляется простой набор данных в PostgreSQL

Документация расположена в url/docs Оттуда можно напрямую подать запрос.

По путям 

* /products

Сервис возвращает список всех продуктов с их категориями
* /categories

Сервис возвращает список категорий с продуктами
* /pairs

Сервис возвращает писок всех пар «Имя продукта – Имя категории»