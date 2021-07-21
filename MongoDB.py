from pymongo import MongoClient
from config import MONGODB_URI

client = MongoClient(MONGODB_URI)
Database = client['Database']
Users = Database['UserID']
Blocked = Database['Blocked']
Index = Database['Index']
Messages =  Database['Messages']

async def saveNewUser(msg):
    dbInfo = {
        '_id':msg.from_user.id,
        'name':f'{msg.from_user.first_name} {msg.from_user.last_name if msg.from_user.last_name!=None else ""}',
        'username':msg.from_user.username
    }

    try: Users.insert_one(dbInfo)
    except: pass

async def getUserIds():
    Ids = Users.distinct('_id')
    return Ids

async def blockedUsers():
    Doc = Blocked.find_one({'_id':0})
    Ids = Doc['users']
    return Ids

async def blockUser(userid):
    try: Blocked.update_one({'_id':0},{'$push':{'users':userid}})
    except: pass

async def unBlockUser(userid):
    try: Blocked.update_one({'_id':0},{'$pull':{'users':userid}})
    except: pass

async def saveMsg(fwd):
    Messages.update_one({'_id':0},{'$push':{'msgs':fwd}})

async def getUser(msg):
    Msgs = Messages.find_one({'_id':0})
    for Msg in Msgs['msgs']:
        if Msg['msg'] == msg:
            return Msg['user']
