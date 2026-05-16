from pydbml.utils.debug import debug

class BreakSignal(Exception):
    debug("[BreakSignal]", "→ CONTINUE TRIGGERED")
    pass

class ContinueSignal(Exception):
    debug("[ContinueSignal]", "→ BREAK TRIGGERED")
    pass