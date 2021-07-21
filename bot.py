from config import *
from MongoDB import *
from pyrogram import Client, filters
from pyrogram.types import *
from apscheduler.schedulers.background import BackgroundScheduler

bot = Client('bot',api_id=API_ID,api_hash=API_HASH,bot_token=TOKEN)

#*--------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command(['start']))
async def start(client,msg):
    if msg.chat.type in ['supergroup','group']:
        return

    await msg.reply(WELCOME.format(name=msg.from_user.first_name))
    await saveNewUser(msg)

#*--------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command(['about']))
async def about(client: Client, msg: Message):
    buttons = [
        [
            InlineKeyboardButton('BUTTON',url='http://www.youtube.com/watch?v=iik25wqIuFo'),
            InlineKeyboardButton('BUTTON',url='http://www.youtube.com/watch?v=iik25wqIuFo'),
        ],
        [
            InlineKeyboardButton('BUTTON',url='http://www.youtube.com/watch?v=iik25wqIuFo')
        ]
    ]

    markup = InlineKeyboardMarkup(buttons)
    await msg.reply(ABOUT,reply_markup=markup)

#*--------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command(['help']))
async def help(client:Client, msg:Message):
    buttons = [
        [
            InlineKeyboardButton('BUTTON',url='http://www.youtube.com/watch?v=iik25wqIuFo'),
            InlineKeyboardButton('BUTTON',url='http://www.youtube.com/watch?v=iik25wqIuFo'),
        ],
        [
            InlineKeyboardButton('BUTTON',url='http://www.youtube.com/watch?v=iik25wqIuFo')
        ]
    ]

    markup = InlineKeyboardMarkup(buttons)
    await msg.reply(HELP,reply_markup=markup)
    
#*-------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command('broadcast'))
async def broadcast(client:Client,msg:Message):
    if not msg.from_user.id in SUDO_USERS:
        await msg.reply('Who tf are you?! Not a Sudo User I see...')
        return
    
    elif not msg.reply_to_message:
        await msg.reply('Reply to a Message which you want to Broadcast Sir.')
        return

    allUsers = await getUserIds()
    totalUsers = len(allUsers)
    usersSent = 0
    for user in allUsers:
        try: await msg.reply_to_message.copy(user)
        except: pass
        else: usersSent += 1
    
    await msg.reply(f'<b>\nTotal Number of Users - {totalUsers}\nMessage Broadcasted to {usersSent} Users.\nFailed to Send to {totalUsers-usersSent} Users.</b>')

#*-------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command('who'))
async def who(client:Client,msg:Message):
    user = msg.from_user
    if msg.reply_to_message:
        if msg.reply_to_message.forward_from:
            user = msg.reply_to_message.forward_from
        elif msg.reply_to_message.forward_sender_name:
            user = await getUser(msg.reply_to_message.message_id)
            user = await client.get_chat(user)
        else:
            user = msg.reply_to_message.from_user            
    
    info = f'''**User Info: ** \n**Name** - {user.first_name} {user.last_name if user.last_name!=None else ""}\n**Username** - {'@' + user.username}\n**ID** - `{user.id}`'''
    await msg.reply(info)


#*-------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command(['block']))
async def block(client:Client, msg:Message):

    if msg.chat.id == ADMIN_CHAT:
        if msg.reply_to_message:
            user = await getUser(msg.reply_to_message.message_id)
            await client.send_message(user,'<b>You\'ve Been Blocked from this Bot, You can\'t message now.</b>')
            await blockUser(user)
            await msg.reply('User Blocked!')

#*-------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message(filters.command(['unblock']))
async def block(client:Client, msg:Message):

    if msg.chat.id == ADMIN_CHAT:
        if msg.reply_to_message:
            user = await getUser(msg.reply_to_message.message_id)
            await client.send_message(user,'<b>You\'ve Been Unblocked, You can message now.</b>')
            await unBlockUser(user)
            await msg.reply('User Unblocked!')

#*-------------------------------------------------------------------------------------------------------------------------------------
@bot.on_message()
async def UserToAdmin(client: Client, msg:Message):
    if msg.chat.id == ADMIN_CHAT:
        if msg.reply_to_message:
            if msg.reply_to_message.from_user.id == BOT_ID:
                if not msg.from_user.id == BOT_ID:
                    if msg.reply_to_message.forward_from:
                        await msg.copy(msg.reply_to_message.forward_from.id)
                    else:
                        user = await getUser(msg.reply_to_message.message_id)
                        await msg.copy(user)

    else:
        if not msg.chat.type in ['supergroup','group']:
            if msg.from_user:
                if not msg.from_user.id == BOT_ID:
                    if not msg.from_user.id in await blockedUsers():        
                        fwd_msg = await msg.forward(ADMIN_CHAT)
                        fwd = {}
                        fwd['msg'] = fwd_msg.message_id
                        fwd['user'] = msg.from_user.id
                        fwd['date'] = msg.date
                        await saveMsg(fwd)
                    
bot.run()
