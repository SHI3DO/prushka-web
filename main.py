from fastapi import FastAPI
import uvicorn
import cogs.db as db

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


MyDB = db.Database()
MyDB.connect("./pru/database.sql")
MyDB.create_table_if_not_exists(table_name='publicchat', fields=['hash', 'content'])
MyDB.create_table_if_not_exists(table_name='user', fields=['userid', 'password', 'token'])

ignored = {"pru"}

from uvicorn.supervisors.watchgodreload import CustomWatcher
class WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update(ignored)
        super(WatchgodWatcher, self).__init__(*args, **kwargs)
uvicorn.supervisors.watchgodreload.CustomWatcher = WatchgodWatcher

import os

for root, dirs, files in os.walk("./cogs"):
    if not '__pycache__' in root:
        for file in files:
            root = root.replace('\\', '/')
            path = f'{root}/{file}'

            module = path.removeprefix('./').replace('/', '.').removesuffix('.py')
            print(f'Loaded : {module}')
            __import__(module)

# 개발시 사용하는 부분입니다. 주석처리만 해둘게요.
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="192.168.0.2", port=7474, reload=True)