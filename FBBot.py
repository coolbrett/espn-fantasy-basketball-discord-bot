class FBBot:

    def __init__(self):
        self.commands = self.__build_commands()
    
    def __build_commands(self):
        #key is command name, value is usage for the command
        commands = {}
        commands["$set-year"] = "$set-year [year]"
        commands["$three-weeks"] = "$three-weeks [week number]"
        commands["$roast"] = "$roast [name]"
        return commands
