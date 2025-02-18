<h1 align="center">Orders Service</h1> 
        
<h2 align="center">Сервис для работы с заказами в ресторанах и кафе</h2>

 Основной стек проекта:
  
      1. Python==3.11
      
      2. Django==4.1.13

      3. Djangorestframework==3.15.2
      
      4. PostgreSQL (DjangoORM)

      5. Docker

<h2 align="left">Для запуска проекта через Docker необходимо:</h2>

• Создать и заполнить файл ```.env``` по шаблону файла ```.env.sample```

• Запустить Docker командой:
```shell
docker compose up --build
```

• Перейдите по url в админ-панель и создайте блюда:
```shell
http://localhost:8000/admin/
```

    Для тестирования API сервиса рекомендуется использовать ```Postman```, 
    файл с коллекцией находится в корне проекта

________________________________________

<h2 align="left">Для запуска проекта без Docker необходимо:</h2>
  
• Установить виртуальное окружение в корневой папке проекта командой:
```shell
python3.11 -m venv venv
```
• Запустить виртуальное окружение командой:
```shell
source venv/bin/activate
```
• Создать в корне проекта файл ```.env``` и заполнить данные по образцу из файла ```.env.sample```

• Установить все необходимые зависимости, указанные в файле ```requirements.txt```:
```shell
pip install -r requirements.txt
```
• Выполнить создание и применение миграций командами:
```shell
python3 manage.py makemigrations
```
```shell
python3 manage.py migrate
```
   
• Создать суперпользователя командой:
```shell
python3 manage.py csu
```

• Запустить сервер командой:
```shell
python3 manage.py runserver
```

• Перейдите по url в админ-панель и создайте блюда:
```shell
http://localhost:8000/admin/
```
________________________________________
## Возможности сервиса

    Сервис имеет веб-интерфейс для работы с заказами
________________________________________
## Эндпоинты для работы с API (Endpoints API)

### Создание заказа

URL: /api/add/

Метод: ```POST```

Пример запроса:

{
    "table_number": int,
    "items": []
}
________________________________________
### Получение списка заказов

URL: /api/list_orders/

Метод: ```GET```
________________________________________
### Получение заказа по ID

URL: /api/retrieve_order/<int:pk>/

Метод: ```GET```
________________________________________
### Изменение заказа

URL: /api/edit_order/<int:pk>/

Метод: ```PUT```

Пример запроса:

{
    "table_number": int,
    "items": [],
    "status": str ("pending", "ready", "paid")
}
________________________________________
### Изменение статуса заказа

URL: /api/edit_order/<int:pk>/

Метод: ```PATCH```

Пример запроса:

{
    "status": str ("pending", "ready", "paid")
}
________________________________________
### Удаление заказа

URL: /api/delete_order/<int:pk>/

Метод: ```DELETE```
________________________________________

### Удачи!
