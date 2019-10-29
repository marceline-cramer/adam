# Adam
Adam is a Discord bot that can host Zandronum sessions and echo game events to and from Discord.

Adam was originally named after Commander Adam Malkovich from the Metroid series, and was created to serve as a Discord frontend for Zandronum on the Metroid Dreadnought server.

If you'd like to contact me about the bot, send me a friend request `@straw_man (CrazyWazy)#5915`, or join the Metroid Dreadnought server (https://discord.gg/KHaGJe3), where I'm active.

## Features

The program works by piping input and output from the Zandronum server process to and from a Discord bot. All messages from Zandronum are then sent to a specified Discord channel. Discord members can then, in the same channel, send messages to Zandronum.

Messages starting with `.` will be echoed in Zandronum as server messages. If a member with nickname `"S H O D A N"` types `.the quick brown fox`, then there will be a message in-game: `<server>: S H O D A N: the quick brown fox`

Messages starting with `?` are processed as Zandronum server commands. To use commands, the member using them must have the Zandronum Admin role, specified with an ID from the command line. A Zandro Admin typing `?changemap metdm02` will send the command `changemap metdm02` to Zandronum.

The feature to add configuration files and modify them from Discord is a WIP.

## To Run

To run Adam, execute `main.py` with the following parameters:

```
-c, --channel: Discord channel ID for the bot
-m, --modrole: Discord moderator role ID; allows admin privileges for Zandronum
-t, --token: Discord bot token
-w wads [wads ...], --wads wads [wads ...]: WADs to load by default
-d directory, --directory directory: Path to directory containing Zandronum and its files
-i iwad, --iwad iwad: IWAD to load
```

Example:
`$ ./main.py -c 012345678901234567 -m 012345678901234567 -t 0123456789abcdefghijklmno.012345.0123456789abcdefghijklmnopqr -w udmx.wad MetroidDreadnought-v1.1.pk3`

Parameters are meant to be specified per-server, as it currently only allows for one output channel at a time. Additionally, you'll need to make a Discord bot, and use its token for the `-t` parameter.

## To-do
- Add `.conf` files
- Fix message length limit formatting
- Fix code injection vulnerability allowing non-Admins to run server commands from Discord
- Option to change command prefixes?
- Class for managing Zandronum output queues
- Class for handling default files/directories?
