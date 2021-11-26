![yamdb_final workflow](https://github.com/codeaudio/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
#api_yamdb  
система рейтинга и отзывов к различным объектам
***
* 1 Установить Git

* 2 Сгенерировать SSH ключ

* 3 Добавить ключ

* 4 клонировать репо git clone ...

* 5 установить docker

* 6 создайте и активируйте окружение(venv)

* 7 собирите контейнер  docker-compose build

* 8  docker-compose up — запуск приложение или docker-compose up -d — запуск приложение в фоновом режиме
  
    ```
    * 1 docker-compose stop - остановка запущенных контейнеров
    
    * 2 docker-compose down - остановка и удаление контейнеров
    ```
* 9 docker-compose exec web python manage.py migrate --noinput - применить миграции

* 10 docker-compose exec web python manage.py createsuperuser - создать суперюзера

* 11 docker-compose exec web python manage.py collectstatic --no-input - собрать статику
  * статику можно не собирать(при пбосрке докера собирается)
  
* 12 docker exec -it <CONTAINER ID> bash - вход в контейнер (проверить файлы проекта)```
    ```
    * 1 docker ps (можно увидеть и скопировать id нужного контейнера)
    ```
* final: http://127.0.0.1/admin проект должен быть доступен локально

```
* документаиця API https://codeaudio.github.io/api_yamdb_api_doc 
или http://127.0.0.1/redoc/
```
