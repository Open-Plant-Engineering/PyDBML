from pydbml.utils.debug import debug

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

class GoLabelSignal(Exception):
    def __init__(self, label):
        self.label = label

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value