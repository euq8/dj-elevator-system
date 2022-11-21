# dj-elevator-system
Elevator System APIs implemented in Django

- mkdir elevator-system && cd elevator-system
- git clone git@github.com:euq8/dj-elevator-system.git  # SSH CLONE

### Open $HOME/elevator-system in VSCode and run following commands in Terminal
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install pip --upgrade (optional)
4. pip install -r requirements.txt

### Open another Terminal, and write following commands to create a db and elvsys schema
> Open PostgreSQL with default user and password (both as postgres), and with default db postgres.
> Create Database and Schema as mentioned in **DATABASES** in *elevatorSystem/settings.py* module.
> 
```
>> psql -h localhost -p 5432 -d postgres -U postgres # enter "postgres" on prompt
>> CREATE DATABASE IF NOT EXISTS dj_db; # create a database
>> \l # list database to verify
>> \c dj_db # connect to database
>> CREATE SCHEMA IF NOT EXISTS elvsys; # create schema "elvsys"
>> \q  # exit from database
```

### In the first terminal in VSCode, run following commands
```
>> python3 manage.py makemigrations # create all migrations from models 
>> python3 manage.py migrate # migrate all migrations to PostgreSQL
>> python3 manage.py runserver # run server to serve apis
```

## API Docs

1. GET: *list-all-active-elevator-requests*
```
url = "http://localhost:8000/elevator-system/requests/"
```

2. GET *fetch-requests-for-specific-elevator*
```
url = "http://localhost:8000/elevator-system/requests/3"
```

3. POST *create-external-request*
```
url = "http://localhost:8000/elevator-system/external-request/"
payload = {
    "floor": 4,
    "direction": "UP",
    "elevator_id": 2
}
```

5. POST *create-internal-request*
```
url = "http://localhost:8000/elevator-system/internal-request/"
payload = {
    "floor": 5,
    "elevator_id": 2
}
```

6. POST *create-N-elevators*
```
url = "http://localhost:8000/elevator-system/elevator/"
payload = {
    "total_elevators": 5
}
```

7. GET *list-all-elevators*
```
url = "http://localhost:8000/elevator-system/elevator/"
```

8. PUT *update-an-elevator-by-id*
```
url = "http://localhost:8000/elevator-system/elevator/"
payload = {
    "id": 5,
    "floor": 5,
    "state": "moving",
    "direction": "down"
}
```

9. GET *nextfloor/<elevator_id>*
```
url = "http://localhost:8000/elevator-system/nextfloor/3"
```

10 .GET *direction/<elevator_id>*
```
url = "http://localhost:8000/elevator-system/direction/3"
```

11. PUT *opendoor/<elevator_id>*
```
url = "http://localhost:8000/elevator-system/opendoor/2/"
```

12. PUT *closedoor/<elevator_id>*
```
url = "http://localhost:8000/elevator-system/closedoor/2/"
```

13. PUT *doorhinderance/<elevator_id>*
```
url = "http://localhost:8000/elevator-system/doorhinderance/2/"
```
