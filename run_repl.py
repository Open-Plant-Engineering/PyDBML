
import sys
import os

# ✅ Add this line
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from pydbml.cli.repl import PyDBMLREPL

if __name__ == "__main__":
    PyDBMLREPL().start()