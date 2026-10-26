from pathlib import Path
import json,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
APP=ROOT.parents[1]/'Ung_Dung/polypweb/polypweb';DEST=HERE/'project'
DEST.mkdir(exist_ok=True)
for name in ['pom.xml','mvnw','mvnw.cmd']:
    shutil.copy2(APP/name,DEST/name)
for name in ['src','.mvn']:
    shutil.copytree(APP/name,DEST/name,dirs_exist_ok=True)
for name in ['logs','runtime','screenshots','storage','mongo_data']:(HERE/name).mkdir(exist_ok=True)
(HERE/'boot_ai.py').write_text('''import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
source=root.parents[1]/"Ung_Dung/polypweb/polypweb/ai-service"
sys.path.insert(0,str(source))
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
os.environ["YOLO_CONFIG_DIR"]=str(Path(__file__).resolve().parent/"runtime/yolo")
os.environ["MPLCONFIGDIR"]=str(Path(__file__).resolve().parent/"runtime/mpl")
import torch
torch.set_num_threads(2)
torch.set_num_interop_threads(1)
import uvicorn
uvicorn.run("main:app",host="127.0.0.1",port=18000,log_level="info")
''',encoding='utf-8')
print('Prepared isolated project',DEST)
