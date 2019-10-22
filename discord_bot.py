#!/usr/bin/python3
import discord
import asyncio

MAXMESSAGELENGTH = 1500

class AdamBot(discord.Client):
    def run(self, zandronum, channelid, modid, token):
        self.zandronum = zandronum
        self.channelid = channelid
        self.modid = modid
        self.loop.create_task(self.zandronumHandler())
        super().run(token)
    async def zandronumHandler(self):
        await self.wait_until_ready()
        print("Handling Zandronum...")

        self.outputChannel = self.get_channel(self.channelid)
        await self.outputChannel.send("Ready to start.")

        while not self.is_closed():
            await asyncio.sleep(1)
            if not self.zandronum.isReady():
                continue

            sout, serr = self.zandronum.getOutput()
            while len(sout) > 0 or len(serr) > 0:
                messageSout = ''
                messageSerr = ''

                while len(messageSout)+len(messageSerr) < MAXMESSAGELENGTH and len(sout)+len(serr) > 0:
                    if len(sout) > 0:
                        messageSout += sout.pop(0)
                    if len(serr) > 0:
                        messageSerr += serr.pop(0)

                message = messageSout
                if messageSerr != '':
                    message += str(" **ERROR: %s**" % (messageSerr))
                message = str(str.encode(message).decode('unicode_escape'))

                print(message)
                await self.outputChannel.send(message)
        print("No longer handling Zandronum.")
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    async def on_message(self, message):
        if message.channel.id != self.channelid or message.author.bot:
            return

        print(message.author.nick, message.content)

        if message.content.startswith('.'):
            if message.author.nick != None:
                messageAuthor = message.author.nick
            else:
                messageAuthor = message.author.name
            newMessage = "say " + messageAuthor + ": " + message.content[1:]
            self.zandronum.send(newMessage)
        elif message.content.startswith('?'):
            isMod = False
            for authorRole in message.author.roles:
                if authorRole.id == self.modid:
                    isMod = True
                    break
            if not isMod:
                errorMessage = message.author.mention + ", you don't have the right role to run server commands. Ping a Zandronum Admin."
                await self.outputChannel.send(errorMessage)
            else:
                commandRaw = message.content[1:]
                params = commandRaw.split()
                if params[0].lower() == "start":
                    self.zandronum.start()
                elif params[0].lower() == "stop":
                    self.zandronum.shutDown()
                elif params[0].lower() == "c" or params[0].lower() == "config":
                    self.zandronum.config.configure(params[1:])
                elif params[0].lower() == "save":
                    self.zandronum.config.save(params[1:])
                elif params[0].lower() == "list":
                    self.zandronum.config.list(params[1:])
                else:
                    self.zandronum.send(commandRaw)
