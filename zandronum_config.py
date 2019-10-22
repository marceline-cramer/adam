#!/usr/bin/python3

import random

gameModes = ['deathmatch', 'duel', 'teamgame', 'teamplay', 'ctf', 'lastmanstanding', 'teamlms', 'terminator', 'oneflagctf', 'skulltag', 'invasion', 'survival', 'posession', 'teamposession']

defaultSettings = {
'maplist':'',
'clearmaplist':'',
'sv_defaultdmflags':'true',
    'fraglimit':'25',
    'sv_maxplayers':'32',
    'sv_maxclients':'32',
    'shuffle':'false'
}

class ZandronumConfiguration:
    def __init__(self, directory, parentEcho=None):
        self.directory = directory
        self.parentEcho = parentEcho
        self.settings = dict(defaultSettings)
        self.maps = []
        self.mode = gameModes[0]
        self.lastConfig = "default"
        self.dirty = False
    def configure(self, args):
        self.echo(str(args))
        var = args[0].lower()
        params = args[1:]

        if var == 'addmap':
            for map in params:
                self.maps.append(map)
        elif var == 'mode':
            newMode = params[0].lower()
            if newMode in gameModes:
                self.mode = newMode
            else:
                self.echo("Invalid game mode `" + newMode + "`.")
        elif var == 'shuffle':
            newShuffle = params[0].lower()
            if newShuffle == 'true' or newShuffle == 'false':
                self.settings['shuffle'] = newShuffle
            else:
                self.echo("`shuffle` must be either `true` or `false`.")
        else:
           self.settings[var] = params[0]

        self.dirty = True
    def save(self, configFile):
        configPath = self.load(configFile, directoryOnly=True)
        self.echo("Saving to `"+configPath + "`")
        f = open(configPath, "w")
        for var in self.settings.keys():
            f.write(str(var) + " " + self.settings[var] + '\n')
        mapList = list(self.maps)
        if self.settings['shuffle'] == "true":
            random.shuffle(mapList)
        for map in mapList:
            f.write("addmap " + map + "\n")
        f.write(self.mode + " 1\n")
        f.close()

        self.dirty = False

        return configPath
    def load(self, configFile=None, directoryOnly=False):
        configPath = self.lastConfig

        if configFile:
            configPath = self.directory + configFile + ".cfg"

        if not directoryOnly:
            if self.dirty:
                backupName = "temp" + str(abs(hash(frozenset(self.settings.values()))+hash(frozenset(self.maps))))[0:4]
                self.echo("Saving temporary config to `" + backupName + "`")
                backupPath = self.save(backupName)
                self.lastConfig = backupPath
            if not configFile:
                configPath = self.lastConfig
            else:
                configPath = self.directory + configFile + ".cfg"
        self.dirty = False
        self.echo("Loaded from `" + configPath + "`")

        return configPath
    def list(self, args):
        outMessage = ""
        outMessage += "Map configurations:\n```"
        for var in sorted(self.settings.keys()):
            outMessage += var+" "+self.settings[var]+"\n"
        outMessage += "```\nMap list:\n```"
        for map in self.maps:
            outMessage += map + "\n"
        outMessage += "```\nGame mode: `"+self.mode+"`\n"
        self.echo(outMessage)
    def echo(self, message):
        if self.parentEcho:
            self.parentEcho(message)
        else:
            print(message)
