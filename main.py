#!/usr/bin/python3

import discord_bot
import zandronum
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--channel", help="Discord channel ID for the bot", required=True, type=int)
parser.add_argument("-m", "--modrole", help="Discord moderator role ID; allows admin privileges for Zandronum", required=True, type=int)
parser.add_argument("-t", "--token", help="Discord bot token", required=True)
parser.add_argument("-w", "--wads", help="WADs to load by default", nargs='+')
args = parser.parse_args()

print(type(args), args, str(args))

zandro = zandronum.Zandronum()
for wad in args.wads:
    zandro.addWad(wad)

client = discord_bot.AdamBot()
client.run(zandro, args.channel, args.modrole, args.token)
zandro.shutDown()
