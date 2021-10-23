from main import app
from main import MyDB


def generate_hash():
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


@app.put("/publicchat", tags=['Public Chat'])
async def add_chat(content: str):
    """
    서버에 원하는 채팅 콘텐츠를 넣습니다
    {'content': content, 'hash': hash}
    """
    vals = {'content': content, 'hash': generate_hash()}
    MyDB.insert(table_name='publicchat', values=vals)
    return vals['hash']


@app.get('/publicchat', tags=['Public Chat'])
async def get_chats(hash=None):
    """
    해시값을 받지 않았다면 10개를 반환하며,
    해시값을 받았다면 해시값 전까지 전부 다 반환합니다
    """
    if not hash:
        ret = MyDB.select(table_name='publicchat', field_names=['hash','content'], limit=10, order="hash DESC")
    elif hash:
        ret = MyDB.select(table_name='publicchat', field_names=['hash','content'], condition=f"hash > {hash}", order="hash DESC")
    ret.reverse()
    return ret


@app.get('/savedb')
async def save():
    """
    SQL 파일에 데이터를 저장합니다
    """
    MyDB.save()
    return 'Saved'