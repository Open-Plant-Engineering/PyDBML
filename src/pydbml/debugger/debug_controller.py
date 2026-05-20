class DebugController:
    def __init__(self):
        self.commands = []
        self.index = 0

    def add_commands(self, cmds):
        self.commands.extend(cmds)

    def set_commands(self, cmds):
        self.commands = list(cmds)
        self.index = 0

    def append_command(self, cmd):
        self.commands.append(cmd)

    def get_next_command(self):
        if self.index < len(self.commands):
            cmd = self.commands[self.index]
            self.index += 1
            return cmd
        return None

    def peek_next_command(self):
        if self.index < len(self.commands):
            return self.commands[self.index]
        return None

    def has_commands(self):
        return self.index < len(self.commands)

    def reset(self):
        self.commands = []
        self.index = 0

    def on_pause(self, state):
        pass  # future hook