class BreakSignal(Exception):
    print("→ CONTINUE TRIGGERED")
    pass

class ContinueSignal(Exception):
    print("→ BREAK TRIGGERED")
    pass