import asyncio
from discord.ext import tasks

async def create_member_to_list(client, broadCastGroup, mainChannel):
    member_list = []
    
    async for member in client.iter_participants(broadCastGroup, aggressive=True):
        if not await check_isMember_on_main(client, member, mainChannel):
            member_list.append(member)
            
    return member_list


async def check_isMember_on_main(client, memberToCheck, mainChannel):
    channel = await client.get_entity(int(mainChannel))
    
    async for member in client.iter_participants(channel, aggressive=True):
        if memberToCheck.id == member.id:
            return True
        
    return False

@tasks.loop(seconds= 20)
async def register_members_to_db(database, client, broadCastGroup, mainGroup):
        member_list = await create_member_to_list(client, broadCastGroup, mainGroup)
        database.delete_database()
        database.create_new_database()
        
        for member in member_list:
            if not database.exists(member.id):
                database.push(member.id, member.first_name, member.username)       
        

        
        
async def Thread_creating_db(database, client, broadCastGroup, mainGroup):
        register_members_to_db.start(database, client, broadCastGroup, mainGroup)    
       


async def is_exist(client, broadCastGroup, id):
    async for member in client.iter_participants(broadCastGroup, aggressive=True):
        if id == member.id:
            return True
        
    return False

def is_private_message(event):
    if event.is_private:
        return True
    
    else: 
        return False
    
def is_admin(sender, admin):
    if sender == admin:
        return True
    else:
        return False
        
        

