class PluginObject:
    def __init__(self, obj):
        self.obj = obj

    # ✅ Forward attribute access
    def __getattr__(self, name):
        return getattr(self.obj, name)

    # ✅ Optional: repr for debugging
    def __repr__(self):
        return repr(self.obj)

