# The Ping of The Pong
Is an API wich recives a request and throw back a new request to complementary API ["The Pong of The Ping"](https://github.com/Fiddelis/c14-pong)

## Instalation
### Initial configuration

1. Install Python
Follow the installation in [Python Download](https://www.python.org/downloads)

2. Install Poetry
Follow the installation in [Poerty Download](https://python-poetry.org/docs/#installation)

### How to Install
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

## Conflict Resolution
The merge conflict was resolved via GitHub.

## How to run tests
```
poetry run pytest
```

## Tests passing
```
poetry run pytest
=========================================================================== test session starts ============================================================================
platform win32 -- Python 3.13.7, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\pedro.freitas\dev\01 - INATEL\C14
configfile: pyproject.toml
plugins: anyio-4.10.0, asyncio-1.1.0, mock-3.14.1
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 20 items                                                                                                                                                          

tests\unit\test_services\test_user_service.py ....................                                                                                                    [100%]

============================================================================ 20 passed in 0.34s ============================================================================
```

## Tests fail (commit hash: 208262d)
```
poetry run pytest 
=========================================================================== test session starts ============================================================================
platform win32 -- Python 3.13.7, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\pedro.freitas\dev\01 - INATEL\C14
configfile: pyproject.toml
plugins: anyio-4.10.0, asyncio-1.1.0, mock-3.14.1
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 20 items                                                                                                                                                          

tests\unit\test_services\test_user_service.py .FF.................                                                                                                    [100%]

================================================================================= FAILURES ================================================================================= 
_________________________________________________________________________ test_login_invalid_user __________________________________________________________________________ 

user_service = <c14_ping.services.user_service.UserService object at 0x00000214E5F1E350>, user_repository = <AsyncMock id='2288780669152'>

    @pytest.mark.asyncio
    async def test_login_invalid_user(user_service, user_repository):
        user_repository.get_by_email.return_value = None
        with pytest.raises(InvalidCredentialsException):
>           await user_service.login("pedro@example.com", "wrong")

tests\unit\test_services\test_user_service.py:35:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  

self = <c14_ping.services.user_service.UserService object at 0x00000214E5F1E350>, email = 'pedro@example.com', password = 'wrong'

    async def login(self, email: str, password: str) -> TokenOut:
        user_on_db = await self.user_repository.get_by_email(email)

        access_token = create_access_token(
>           subject=user_on_db.email,
                    ^^^^^^^^^^^^^^^^
            roles=user_on_db.role_names,
        )
E       AttributeError: 'NoneType' object has no attribute 'email'

src\c14_ping\services\user_service.py:23: AttributeError
________________________________________________________________________ test_login_wrong_password _________________________________________________________________________ 

user_service = <c14_ping.services.user_service.UserService object at 0x00000214E5F1F9D0>, user_repository = <AsyncMock id='2288780667472'>
fake_user = <MagicMock name='mock.get_by_id()' id='2288780668480'>

    @pytest.mark.asyncio
    async def test_login_wrong_password(user_service, user_repository, fake_user):
        user_repository.get_by_email.return_value = fake_user

        with patch(f"{USER_SERVICE_PATH}.verify_password", return_value=False):
            with pytest.raises(InvalidCredentialsException):
>               await user_service.login("pedro@example.com", "wrong")

tests\unit\test_services\test_user_service.py:44:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  

self = <c14_ping.services.user_service.UserService object at 0x00000214E5F1F9D0>, email = 'pedro@example.com', password = 'wrong'

    async def login(self, email: str, password: str) -> TokenOut:
        user_on_db = await self.user_repository.get_by_email(email)

>       access_token = create_access_token(
            subject=user_on_db.email,
            roles=user_on_db.role_names,
        )
E       TypeError: create_access_token() missing 1 required positional argument: 'expires_delta'

src\c14_ping\services\user_service.py:22: TypeError
========================================================================= short test summary info ========================================================================== 
FAILED tests/unit/test_services/test_user_service.py::test_login_invalid_user - AttributeError: 'NoneType' object has no attribute 'email'
FAILED tests/unit/test_services/test_user_service.py::test_login_wrong_password - TypeError: create_access_token() missing 1 required positional argument: 'expires_delta'   
======================================================================= 2 failed, 18 passed in 0.49s =======================================================================
```

## Tests passing again (commit hash: 5f5814d)
```
poetry run pytest 
=========================================================================== test session starts ============================================================================
platform win32 -- Python 3.13.7, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\pedro.freitas\dev\01 - INATEL\C14
configfile: pyproject.toml
plugins: anyio-4.10.0, asyncio-1.1.0, mock-3.14.1
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 20 items                                                                                                                                                          

tests\unit\test_services\test_user_service.py ....................                                                                                                    [100%]

============================================================================ 20 passed in 0.30s ============================================================================
```
