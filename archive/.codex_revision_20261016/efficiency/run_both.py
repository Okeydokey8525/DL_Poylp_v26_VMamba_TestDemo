from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
for name in ['baseline','tsvm']:
    subprocess.run([sys.executable,str(here/'measure.py'),name],check=True)
