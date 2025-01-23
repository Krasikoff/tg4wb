# Описание тестового задания.

pdf- файл в корне репозитория.

# Решение.

Выполнил стандартные работы согласно заданию. Подключил fastapi-users.
Зарегистрироваться может любой пользователь, авторизированному пользователю
доступны все endpoint. 

## запуск приложения.

- Клонируем репозиторий.

```shell
git@github.com:Krasikoff/tg4wb.git
```

- Запуск postgres. Переходим в соотвтетствующую директрорию.
(предположительно докер установлен, sudo перед docker в зависимости от настроек и os )
```shell
cd postgres
docker compose up -d
```

Проверка БД.
```shell
psql -h localhost -p 5432 -U postgres -W postgres

```
Проверка pgadmin.
```shell
http://localhost:5050
cd ..
```

## Запуск backend-приложения в docker режиме.
(не забываем создать файл .env как в env.example!!!)

```shell
docker build -t tg4wb .
docker run -d --name tg4wb -p 8000:8000 tg4wb
docker exec -it tg4wb alembic upgrade head
```

- Все в одном 
(не забыть выключить контейнеры, если проверяли по очереди. переходим в соответствующую директорию и выключаем.) 
```shell
cd <dir>
docker compose down
```

```shell
docker compose up -d
docker exec -it tg4wb-server-1 sh
alembic upgrade head
exit
```

Проверяем работу. 
```shell
http://localhost:8000/docs/
```


## в develop режиме.
- Устанавливаем окружение.
```shell
python -m venv venv && source venv/bin/activate
```
- Устанавливаем заисимости.
```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Запуск приложения.
```shell
uvicorn app.main:app --reload 
```


to be continued....

### Команды alembic - справочно 

```shell
alembic init --template async alembic
alembic revision --autogenerate -m "First migration" 
alembic upgrade head
```
