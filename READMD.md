# fast-chess-game-service

How to run server:

- create venv

```bash
python -m venv venv
source venv/bin/activate (Linux)
source venv/Scripts/activate (Windows)
pip install -r requirements.txt
```

- run app

```bash
cd fast-chess-game-service
python manage.py makemigrations rest_api
python manage.py makemigrations
python manage.py migrate
docker run -p 6379:6379 -d redis:7
python manage.py runserver
```
