# MUD API

API для для маленького MUD (Multi-user dungeon) без регистрация пользователей.


## Запуск

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте БД командой `python3 manage.py migrate`
- Запустите сервер командой `python3 manage.py runserver`

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
```
DEBUG='True' # Режим отладки true или false
ENGINE='django.db.backends.sqlite3' # движок базы данных
HOST='database_name.google.com' # хост базы данных
PORT='8080' # порт базы данных
NAME='database_name' #название базы данных
USER='user_name' # Имя пользователя
PASSWORD='12345' # Пароль
SECRET_KEY='asdsde12312' # секретный ключ, с помощью которого шифруют пароли пользователей сайта
```
## Примеры использования
Доступны следующие вызовы http:
- получать список комнат  
GET-запрос  
/api/rooms/
- получать список персонажей  
GET-запрос   
/api/characters/  
- получать описание комнаты  
GET-запрос  
/api/rooms/<id комнаты>/description
- получать список персонажей в комнате  
GET-запрос  
/api/rooms/<id комнаты>/chars
- получать список предметов в комнате  
GET-запрос  
/api/rooms/<id комнаты>/items
- переводить персонажа из комнаты в комнату  
PUT-запрос  
/characters/<id персонажа>/room  
Пример тела запроса:  
{
'room': 1
}
- подбирать персонажем предметы из комнаты в инвентарь  
PUT-запрос  
/characters/<id персонажа>/take_item  
Пример тела запроса:  
{
    "items": [1,2]
}
- выкладывать предметы из инвентаря персонажа в комнату  
PUT-запрос  
/characters/<id персонажа>/put_out_item  
Пример тела запроса:  
{
    "items": [1,2]
}


## Цели проекта

Код написан в качестве тестового задания для [Factory5](http://factory5.ai/).
