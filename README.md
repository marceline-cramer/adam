# Adam
Adam is a Discord bot that can host Zandronum sessions and echo game events to and from Discord.

Adam was originally named after Commander Adam Malkovich from the Metroid series, and was created to serve as a Discord frontend for Zandronum on the Metroid Dreadnought server.

If you'd like to contact me about the bot, send me a friend request `@straw_man (CrazyWazy)#5915`, or join the Metroid Dreadnought server (https://discord.gg/KHaGJe3), where I'm active.

## To Run

To run Adam, execute `main.py` with the following parameters:

```
-c, --channel: Discord channel ID for the bot
-m, --modrole: Discord moderator role ID; allows admin privileges for Zandronum
-t, --token: Discord bot token
-w wads [wads ...], --wads wads [wads ...]: WADs to load by default
```

Example:
`$ ./main.py -c 012345678901234567 -m 012345678901234567 -t 0123456789abcdefghijklmno.012345.0123456789abcdefghijklmnopqr -w udmx.wad MetroidDreadnought-v1.1.pk3`

Parameters are meant to be specified per-server, as it currently only allows for one output channel at a time. Additionally, you'll need to make a Discord bot, and use its token for the `-t` parameter.

Zandronum and all of its files (including optional WADs) must be in a subfolder named `zandronum/` in the same directory as `main.py`.

## To-do
- Add `.conf` files
- Comment and format existing code
- Fix message length limit formatting
- Fix code injection vulnerability allowing non-Admins to run server commands from Discord
