from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from pydbml.core.engine import Engine


class PyDBMLREPL:
    """
    Interactive REPL interface for PyDBML
    """

    def __init__(self):
        self.engine = Engine()
        self.session = PromptSession(history=InMemoryHistory())

    def start(self):
        print("PyDBML Engine Started (type exit/quit to exit)\n")

        while True:
            try:
                code = self.session.prompt("PyDBML >> ")

                if code.strip().lower() in ("exit", "quit"):
                    break

                if not code.strip():
                    continue

                result = self.engine.execute(code)

                if result is not None:
                    print(result)

            except KeyboardInterrupt:
                continue

            except EOFError:
                print("\nExiting...")
                break

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    PyDBMLREPL().start()
