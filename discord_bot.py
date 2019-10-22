#!/usr/bin/python3

import discord
import asyncio

MAXMESSAGELENGTH = 1500

class AdamBot(discord.Client):
    # Initialization
    def run(self, zandronum, channelid, modid, token):
        self.zandronum = zandronum
        self.channelid = channelid
        self.modid = modid

        # Process Zandronum output in our event loop
        self.loop.create_task(self.zandronumHandler())

        # Run the client even loop as normal
        super().run(token)

    # Asynchronous loop for processing Zandronum's
    # output and echoing it to Discord
    async def zandronumHandler(self):
        # Wait for the client to start
        await self.wait_until_ready()
        print("Handling Zandronum...")

        self.outputChannel = self.get_channel(self.channelid)
        await self.outputChannel.send("Ready to start.")

        while not self.is_closed():
            # Cap to 1 FPS
            await asyncio.sleep(1)

            # If Zandronum isn't running, skip the loop
            if not self.zandronum.isReady():
                continue

            # Dump the output queue to Discord
            sout, serr = self.zandronum.getOutput()
            while len(sout) > 0 or len(serr) > 0:
                messageSout = ''
                messageSerr = ''

                # Pop from the output until we've
                # filled up a message
                while len(messageSout)+len(messageSerr) < MAXMESSAGELENGTH and len(sout)+len(serr) > 0:
                    if len(sout) > 0:
                        messageSout += sout.pop(0)
                    if len(serr) > 0:
                        messageSerr += serr.pop(0)

                # Put it together, with errors
                message = messageSout
                if messageSerr != '':
                    message += str(" **ERROR: %s**" % (messageSerr))

                # Escape the message properly
                message = str(str.encode(message).decode('unicode_escape'))

                # Output to Discord
                print(message)
                await self.outputChannel.send(message)
        print("No longer handling Zandronum.")

    # Login event
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # Discord client event for receiving a message
    async def on_message(self, message):
        # Make sure we're processing the right message
        if message.channel.id != self.channelid or message.author.bot:
            return

        # If the message starts with a ".",
        # send the message to Zandronum
        if message.content.startswith('.'):
            if message.author.nick != None:
                messageAuthor = message.author.nick
            else:
                messageAuthor = message.author.name
            newMessage = "say " + messageAuthor + ": " + message.content[1:]
            self.zandronum.send(newMessage)
        # If the message starts with a "?",
        # run commands
        elif message.content.startswith('?'):
            # Check the author's roles for the admin role
            isMod = False
            for authorRole in message.author.roles:
                if authorRole.id == self.modid:
                    isMod = True
                    break

            if not isMod:
                errorMessage = message.author.mention + ", you don't have the right role to run server commands. Please ping a Zandronum Admin."
                await self.outputChannel.send(errorMessage)
            else:
                # Parse the message
                commandRaw = message.content[1:]
                params = commandRaw.split()

                # Run the command
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
