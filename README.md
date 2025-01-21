# beresnev_tz4

# Описание тестового задания.

pdf- файл в корне репозитория.

# Решение.

Выполнил стандартные работы по заданию. Работа с refresh_token - ом в том виде в котором она в боьшинстве случаев используется.
Хранится отдельно на redis, имеет срок боьший чем access токен, используется для перевыпуска access_token.
Для использования его так же как access_token при доступе к роутерам, необходима дополнительное обсуждение. Возможно написание функции с встраиванием Depency... 

с AIOHTTP немного не понял, предположил, что это frontend сервер. Сделал fake-front-hello и под него контейнер.

## запуск приложения.

- Клонируем репозиторий.

```shell
git@github.com:Krasikoff/beresnev_tz4.git
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

- Запуск redis. Переходим в соотвтетствующую директрорию.
```shell
cd redis
docker compose up -d
```

Прверка redis.
```shell
redis-cli -h 127.0.0.1 -p 6379 -a redis
cd ..
```

- Запуск aiohttp. Переходим в соотвтетствующую директрорию.
```shell
cd aiohttp
docker compose up -d
```

Проверка aiohttp
```shell
http://localhost:8080
cd ..
```

## Запуск backend-приложения в docker режиме.
(не забываем создать файл .env как в env.example!!!)

```shell
docker build -t tz4 .
docker run -d --name tz4 -p 8000:8000 tz4
docker exec -it tz4 alembic upgrade head
```

- Все в одном 
(не забыть выключить контейнеры, если проверяли по очереди. переходим в соответствующую директорию и выключаем.) 
```shell
cd <dir>
docker compose down
```

```shell
docker compose up -d
docker exec -it beresnev_tz4-server-1 sh
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
git push -u origin main && source venv/bin/activate
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


Проверка redis.

```shell
redis-cli -h 127.0.0.1 -p 6379 -a redis
```
```shell
redis> set test:1:string "my binary safe string" OK
```
```shell
redis> get test:1:string "my binary safe string"
```
