from telethon import TelegramClient, events,Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.sync import TelegramClient
from telethon.tl.types import InputUser
 
import help_func
import asyncio
import Database

class Bot:
    def __init__(self, config):
        
        self.config_bot = config
        self.client = TelegramClient("session", self.config_bot["api_id"], self.config_bot["api_hash"]).start(bot_token = self.config_bot["bot_token"])
        self.broadcastChannel = config["broadcast_Channel_id"]
        self.mainChannel = config["main_channel_id"]
        self.server = Database.database()

        @self.client.on(events.NewMessage(pattern='/start'))
        async def help_event(event):
            sender = await event.get_sender()
            sender_id = sender.id
            
            showusers = self.config_bot["show_users_command"]
            banall = self.config_bot["ban_all_users_command"]
            banuser = self.config_bot["ban_user_command"]
            
            text_help = f"Commands:\n" \
                "\"{showusers}'\" -> show every user in the channel.\n" \
                "\"{banall}'\" -> ban every user in the channel.\n" \
                "\"{banuser}'\"-> ban a user by their id."

            text_help = text_help.format(**locals())
                
            await self.client.send_message(sender_id, text_help)


        @self.client.on(events.NewMessage(pattern = self.config_bot["show_users_command"]))
        async def show_users_event(event):
            sender = await event.get_sender()
            sender_id = sender.id
            await self.client.send_message(sender_id, self.server.print_members())
            
            
        @self.client.on(events.NewMessage(pattern=self.config_bot["ban_all_users_command"]))
        async def ban_all_users(event):
            sender = await event.get_sender()
            sender_id = sender.id
            list_of_users = self.server.getid_list()
            
            for user in list_of_users:
                user_to_remove = await self.client.get_input_entity(int(user))
                await self.client.kick_participant(self.broadcastChannel, user_to_remove)
            
            await help_func.register_members_to_db(self.server, self.client, int(self.broadcastChannel), self.mainChannel)
            await self.client.send_message(sender_id, f"Deleted every user from the database")
            
                
            
            
        @self.client.on(events.NewMessage(pattern = self.config_bot["ban_user_command"]))
        async def ban_user_event(event):
            sender = await event.get_sender()
            sender_id = sender.id
            message = event.message
            user_input = message.text.split(" ")

            if len(user_input) < 2:
                await self.client.send_message(sender_id, "Invalid command. Please provide the user ID.")
                return

            user_id = user_input[1]
            
            confirm_message = "Are you sure you want to ban this user?"
            buttons = [
                [Button.inline("Yes", data=f"ban_user_{user_id}"), Button.inline("No", data=f"cancel_ban_user_{user_id}")]
            ]
            await self.client.send_message(sender_id, confirm_message, buttons=buttons)
            
            
        @self.client.on(events.CallbackQuery())
        async def handle_button_click(event):
            sender = await event.get_sender()
            sender_id = sender.id
            data = event.data.decode()
           
            if data.startswith("ban_user_"):
                try:
                    user_id = int(data.split("_")[2])
                    if  await help_func.is_exist(self.client, int(self.broadcastChannel), user_id):
                        user_to_remove = await self.client.get_input_entity(int(user_id))
                        await self.client.kick_participant(int(self.broadcastChannel), user_to_remove)
                        self.server.remove_user(user_id)
                        await self.client.send_message(sender_id, "User has been banned.")
                        
                    else:
                        await self.client.send_message(sender_id, "User Not found.")
                        
                except ValueError:
                     await self.client.send_message(sender_id, "The id you typed is not valid.")
                     return
                

                    
    

            elif data.startswith("cancel_ban_user_"):
                user_id = int(data.split("_")[3]) 
                await self.client.send_message(sender_id, "Ban operation has been canceled.")
        
  
    def run(self):
        asyncio.ensure_future(help_func.Thread_creating_db(self.server, self.client, int(self.broadcastChannel), self.mainChannel)) 
        self.client.run_until_disconnected()
