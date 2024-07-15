# Resource documentation

## API Security and identity management
- https://flask-jwt-extended.readthedocs.io/en/stable/index.html

## Events

- [Example 1](https://stackoverflow.com/questions/42308956/sqlalchemy-how-to-process-a-column-before-it-is-committed?rq=3)

```python
from sqlalchemy.event import listen
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text) # should be a hash

    @staticmethod
    def _hash_password(mapper, connection, target):
        user = target
        user.password = hash_method(user.password)


listen(User, 'before_insert', User._hash_password)
listen(User, 'before_update', User._hash_password)
```
- [Link 1](https://docs.sqlalchemy.org/en/20/core/event.html).
- [Link 2](https://docs.sqlalchemy.org/en/20/orm/extending.html)

## Project structure
```bash
ums/
├── VERSION
├── __init__.py
├── __main__.py
├── api
│   ├── __init__.py
│   ├── application.py
│   ├── common
│   │   └── resource.py
│   ├── lifetime.py
│   ├── modules
│   │   ├── info.md
│   │   └── player
│   │       ├── resource_v1.py
│   │       └── schema.py
│   ├── monitoring.py
│   └── routes
│       ├── __init__.py
│       └── v1.py
├── db
│   ├── __init__.py
│   ├── base.py
│   ├── migrations
│   │   ├── __init__.py
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── player_model.py
│   └── session.py
├── logging.py
├── settings.py
├── static
│   └── foo.txt
└── utils
    └── __init__.py
```

## References
- [Flask docs](https://flask-restful.readthedocs.io/en/latest/intermediate-usage.html#project-structure
)
