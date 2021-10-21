from fastapi import FastAPI
import uvicorn
import database

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


MyDB = database.Database()
MyDB.connect("./pru/publicchat.sql")
MyDB.create_table_if_not_exists(table_name='publicchat', fields=['hash', 'content'])

ignored = {
    "pru",
}

from uvicorn.supervisors.watchgodreload import CustomWatcher


class WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update(ignored)
        super(WatchgodWatcher, self).__init__(*args, **kwargs)


uvicorn.supervisors.watchgodreload.CustomWatcher = WatchgodWatcher

__import__('publicchat')

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.2", port=7474, reload=True)
