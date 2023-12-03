from fastapi import APIRouter, File, UploadFile, BackgroundTasks, Cookie, Response, Header, Request,\
                    HTTPException, status, Depends
from typing import Annotated, Optional
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
import asyncio
from app.models.all import UserModel
from jose import jwt

app = APIRouter()
security = HTTPBasic()


@app.on_event("startup")
async def startup_database():
    await asyncio.sleep(1)


@app.on_event("shutdown")
async def shutdown_database():
    await asyncio.sleep(1)


# фейковая БД для хранения пользовательских данных
fake_database = {
    1: {"id": 1, "name": "John Doe"},
    2: {"id": 2, "name": "Jane Smith"},
}

# Функция зависимости для получения экземпляра базы
def get_database():
    return fake_database



@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile) -> dict | None:
    return {"filename": file.filename}


@app.get("/users/{user_id}")
def read_user(response: Response,
              # request: Request,
              user_id: int,
              is_admin: bool = False,
              session_token: Optional[str] = Cookie(default=None),
              user_agent: Annotated[str | None, Header()] = None,
              database: dict = Depends(get_database)):
    if session_token is None:
        response.headers["Custom-Header"] = "True"
        response.set_cookie(key="session_token", value=":)", expires=10)
        # everything above is ignored
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            headers={"Custom2-Header": "True"})
        # or
        # response.status_code = status.HTTP_401_UNAUTHORIZED
    if user_id in database:
        is_admin = True
    return {"user_id": user_id, "is_admin": is_admin, "session_token": session_token, "ua": user_agent}


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user_pass = "pass"
    if user_pass != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return True


@app.post("/users/")
async def create_user(bt: BackgroundTasks, user: UserModel, authorized: bool = Depends(authenticate_user)) -> UserModel:
    bt.add_task(write_notification, user.email, message="Welcome to the FastAPI users")

    return user

################################# JWT ####################################3
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
USER = None


# Функция получения User'а по токену
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (subject);
        # обычно там еще можно взять "iss" - issuer/эмитент,
        # или "exp" - expiration time - время 'сгорания' и другое, что мы сами туда кладем
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# роут для аутентификации; так делать не нужно, это для примера - более корректный пример в следующем уроке
@app.post("/login")
async def login(user_in: UserModel):
    USER = user_in
    return {"access_token": create_jwt_token({"sub": user_in.name}), "token_type": "bearer"}


# защищенный роут для получения информации о пользователе
@app.get("/about_me")
async def about_me(current_user: str = Depends(get_user_from_token)):
    if USER is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if USER.name != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return USER