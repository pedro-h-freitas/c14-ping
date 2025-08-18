# The Ping of The Pong
Is an API wich recives a request and throw back a new request to complementary API ["The Pong of The Ping"](https://github.com/Fiddelis/c14-pong)

## Initial configuration

1. Install Python
Follow the installation in [Python Download](https://www.python.org/downloads)

2. Install Poetry
Follow the installation in [Poerty Download](https://python-poetry.org/docs/#installation)

## How to Install
1. Clone the repository
```
git clone https://github.com/pedro-h-freitas/c14-ping.git
cd c14-ping
```

2. Install dependencies
```
poetry install
```

## How to run
```
poetry run fastapi run src/c14_ping/main.py --reload
```

## How to build
```
poetry build
```
