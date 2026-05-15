class ObjectInstance:

    def __init__(self, definition):
        self.definition = definition  # ObjectDefNode
        self.value = {}

        # ✅ initialize all members
        for name, type_name in definition.members.items():
            self.value[name] = None   # no default yet
