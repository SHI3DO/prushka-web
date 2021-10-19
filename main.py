from fastapi import FastAPI
import uvicorn

import db

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

MyDB = db.Database()
MyDB.connect("./pru/publicchat.sql")
MyDB.create_table_if_not_exists(table_name='chat', fields=['content'])

@app.get("/publicchat/append/{content}")
async def read_item(content: str):
    dic = {}
    dic['content'] = content
    MyDB.insert(table_name='chat', values=dic)
    ret = MyDB.select(table_name='chat', field_names=['content'])
    rlist = []
    for r in ret:
        rlist.append(r[0])
    return rlist

@app.get('/publicchat/save')
async def save():
    MyDB.save()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=7113)