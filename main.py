from fastapi import FastAPI

app = FastAPI()

f = open("./pru/publicchat.txt", 'w', encoding='UTF-8')
f.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/publicchat/{content}")
async def read_item(content: str):
    k = open("./pru/publicchat.txt", 'a')
    print(content)
    k.write(content + "\n")
    k.close()
    k = open("./pru/publicchat.txt", 'r')
    returnval = k.read()
    k.close()
    return {returnval}
