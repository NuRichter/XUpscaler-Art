import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from xupscaler.deps import ensure_all
ensure_all()

from xupscaler.cli import run
run()
