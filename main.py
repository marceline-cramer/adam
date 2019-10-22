#!/usr/bin/python3

def main():
    import discord_bot
    import zandronum
    import argparse

    # Handle parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--channel", metavar="channelID", help="Discord channel ID for the bot", required=True, type=int)
    parser.add_argument("-m", "--modrole", metavar="modroleID", help="Discord moderator role ID; allows admin privileges for Zandronum", required=True, type=int)
    parser.add_argument("-t", "--token", metavar="bottoken", help="Discord bot token", required=True)
    parser.add_argument("-w", "--wads", metavar="wads", help="WADs to load by default", nargs='+')
    args = parser.parse_args()

    # Start the server and add WADs from arguments
    zandro = zandronum.Zandronum()
    for wad in args.wads:
        zandro.addWad(wad)

    # Create a client and initialize from Zandro
    client = discord_bot.AdamBot()
    client.run(zandro, args.channel, args.modrole, args.token)

    # Shut down after the client closes
    zandro.shutDown()

if __name__ == "__main__":
    main()
