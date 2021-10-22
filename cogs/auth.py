from fastapi import security
from fastapi.param_functions import Depends
from main import app
from main import MyDB

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Security

import hashlib

class AuthHandler:
    security = HTTPBearer()

    def wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        if MyDB.select(table_name='user', field_names=['userid'], condition=f"token = '{auth.credentials}'") == []:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

Auth = Depends(AuthHandler().wrapper)


def hash(value):
    """
    SHA3-512 방식으로 값을 암호화합니다
    """
    return hashlib.sha3_512(value.encode()).hexdigest()


def myhash(value):
    """
    SHA3-512 방식 암호화를 3차례 수행합니다
    """
    return hash(hash(hash(value)))



@app.post('/account', tags=['Account'])
async def register(id = None, pw = None):
    """
    id와 pw로 회원가입을 하고 토큰을 반환합니다
    """
    if id and pw:
        if MyDB.select(table_name='user', field_names=['userid'], condition=f"userid = '{id}'") == []:
            MyDB.insert(table_name='user', values={'userid': id, 'password': myhash(pw), 'token': hash(id + pw)})
            return hash(id + pw)
        else:
            return 'Exists'


@app.get('/account', tags=['Account'])
async def generate_token(id = None, pw = None):
    """
    id와 pw를 바탕으로 토큰을 반환합니다
    """
    if id and pw:
        return hash(id + pw)


# @app.get('/account/test')
# async def accountest(auth = Auth):
#     return True