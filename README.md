# Twitter-Clone-API

## Features

- Users can register and login to their accounts.
- All users can access all posts and its likes.
- Authenticated users can create, edit, delete their own posts and like/unlike posts.
- Authenticated users can follow/unfollow other users

## Technologies

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Postgresql](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Setup

```python
cd root/of/project
pip install -r requirements.txt
```

- Create a .env file in your project root folder and add your variables. See .env.example for assistance.

## Usage

Start the project by running the following commands

```python
cd root/of/project
uvicorn app.main:app
```

The project should run on http://localhost:8000/.
