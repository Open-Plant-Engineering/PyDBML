from pydbml.utils.debug import debug

class BreakSignal(Exception):
    debug("→ CONTINUE TRIGGERED")
    pass

class ContinueSignal(Exception):
    debug("→ BREAK TRIGGERED")
    pass