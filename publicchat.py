from main import app
from main import MyDB


def genHash():
    """
    기존 최신 해시값에 1을 더하여 새로운 해시를 발급해줍니다
    """
    pasthash = MyDB.select(table_name='publicchat', field_names=['hash'], limit=1, order="hash DESC")
    if pasthash == []:
        pasthash = 0
    else:
        pasthash = pasthash[0][0]
    
    hash = pasthash + 1

    return hash


@app.get("/publicchat/append/{content}")
async def read_item(content: str):
    """
    {'content': content, 'hash': hash} 형식으로 서버에 집어넣습니다
    """
    dic = {}
    dic['content'] = content
    dic['hash'] = genHash()
    MyDB.insert(table_name='publicchat', values=dic)
    return dic['hash']

@app.get('/publicchat/get')
async def get_item(hash=None):
    """
    해시값을 받지 않았다면 10개를 반환하며,
    해시값을 받았다면 해시값 전까지 전부 다 반환합니다
    """
    if not hash:
        ret = MyDB.select(table_name='publicchat', field_names=['hash','content'], limit=10, order="hash DESC")
    elif hash:
        ret = MyDB.select(table_name='publicchat', field_names=['hash','content'], condition=f"hash > {hash}")
    return ret


@app.get('/publicchat/save')
async def save():
    """
    SQL 파일에 데이터를 저장합니다
    """
    MyDB.save()

@app.get('/hash')
async def rhash():
    return genHash()