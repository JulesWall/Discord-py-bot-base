import discord
import asyncio

from config import *
from Discord.data.commands import commands

class MessageManager():

    def __init__(self, message, bot):
        self.message = message
        self.bot = bot
        self.is_command = self.check()
    
    async def manage(self):
        if self.check: 
            await self.get_command()
    
    def check(self):
        check = [
            self.message.content.startswith(PREFIX), 
            is_maintenance and self.message.author.id not in MAINTENANCE_AUTHORIZE,
            self.message.guild.id in SERVER_WHITELISTED
        ]
        return False in check
    
    async def get_command(self, dict_args=commands, indice=0):
        strc = str(self.message.content.split(" ")[indice][1:]).lower()

        found = []
        for key in dict_args.keys():
            found.append(key)
        
        for i in range(len(strc)):
            for key in dict_args.keys():
                try: assert key[i] == strc[i]
                except: 
                    if key in found:
                        found.remove(key)
            if len(strc) <= 1: break
        
        if len(found)==1: 
            await dict_args[found[0]][0](self.message, self.bot).run()
            
            