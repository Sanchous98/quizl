# Quizl Tesk Task

Make ```.env``` file, based on ```.env.example```

### Start with docker

```
docker-compose up
```

### Start without docker

```
pip install -r requirements.txt
uvicorn main:app --reload
```

### Working with api

API documentation is available on ```127.0.0.1:8000/docs```

To create a game, you must be logged in as a super user. You can create a super user via CLI tool.
```
python su.py -f <firstname> -l <lastname> -u <username> -e <email> -p <password> -a <is_active> -s <is_super>
```
After you logged in as a super user, you can create a game, using provided api. Every game must have at least 1 question and every question must have at least 2 answers (one of them must be correct). API provides CRUD for every entity, so you can update games, questions and answers whenever you want as well as deleting them, using appropriate requests
