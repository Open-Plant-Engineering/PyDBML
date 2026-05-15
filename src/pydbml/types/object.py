class ObjectInstance:

    def __init__(self, definition):
        self.definition = definition  # ObjectDefNode
        self.value = {}

        # ✅ initialize members
        for name in definition.members:
            self.value[name] = None