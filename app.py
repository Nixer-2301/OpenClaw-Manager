"""OpenClaw Manager v1.2.0 - Edge App Mode"""
import os, sys, json, subprocess, time, tempfile, socket
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE = Path(sys._MEIPASS)
else:
    BASE = Path(__file__).parent

sys.path.insert(0, str(BASE / "python-backend"))

from core.skill_manager import SkillManager
from core.model_manager import ModelManager
from core.plugin_manager import PluginManager
from core.process_manager import ProcessManager
from core.config_manager import ConfigManager
from core.log_manager import LogManager
from core.stats_manager import StatsManager
from core.settings_manager import SettingsManager
from core.openclaw_api import OpenclawAPI

sm=SkillManager(); mm=ModelManager(); pm=PluginManager()
prm=ProcessManager(); cm=ConfigManager(); lm=LogManager()
stm=StatsManager(); sem=SettingsManager(); oa=OpenclawAPI()

def dispatch(m, a):
    try:
        d = a or {}
        if m=="skills.getAll":
            r=sm.scan_skills()
            for s in r:
                ah=s.get("argument_hint","")
                if isinstance(ah,list): s["argument_hint"]=", ".join(str(x) for x in ah)
            return r
        if m=="skills.toggle":
            sks=sm.scan_skills();sk=next((s for s in sks if s.get("path")==d.get("path")),None)
            if sk: sm.toggle_skill(sk); return sm.scan_skills()
        if m=="skills.delete":
            sks=sm.scan_skills();sk=next((s for s in sks if s.get("path")==d.get("path")),None)
            if sk: sm.delete_skill(sk); return sm.scan_skills()
        if m=="skills.import":
            import base64,tempfile as tf
            data=d.get("data","")
            with tf.NamedTemporaryFile(delete=False,suffix=".zip") as f:
                f.write(base64.b64decode(data)); sm.import_skill(f.name)
            return sm.scan_skills()
        if m=="models.getAll": return mm.get_all_models()
        if m=="models.add": mm.add_model(d); return mm.get_all_models()
        if m=="models.delete": mm.delete_model(d.get("provider",""),d.get("id","")); return mm.get_all_models()
        if m=="plugins.getAll": return pm.get_all_plugins()
        if m=="plugins.toggle":
            pls=pm.get_all_plugins();p=next((x for x in pls if x.get("name")==d.get("name")),None)
            if p: pm.toggle_plugin(p); return pm.get_all_plugins()
        if m=="process.getStatus": return prm.get_status()
        if m=="process.getConfig": return prm.get_config()
        if m=="process.start": return prm.start()
        if m=="process.stop": return prm.stop()
        if m=="process.restart": return prm.restart()
        if m=="process.getLogs": return prm.get_logs(d.get("lines",100))
        if m=="config.read": return cm.read_config() or "{}"
        if m=="config.save": return cm.save_config(d.get("content","{}"))
        if m=="config.validate":
            ok,msg=cm.validate_config(d.get("content",""))
            return {"valid":ok,"message":msg}
        if m=="config.backup": cm.create_backup(); return True
        if m=="config.listBackups": return cm.list_backups()
        if m=="config.restore": return cm.restore_backup(d.get("path",""))
        if m=="logs.getFiles": return lm.get_log_files()
        if m=="logs.read": return lm.read_log(d.get("file",""),d.get("level","ALL"),d.get("keyword"))
        if m=="logs.getStats": return lm.get_log_stats(d.get("file",""))
        if m=="stats.getOverview": return stm.get_overview()
        if m=="stats.getDaily": return stm.get_daily_session_stats(d.get("days",7))
        if m=="settings.getAll": return sem.get_all()
        if m=="settings.save":
            for k,v in d.items():
                if isinstance(v,dict) and k in ("general","paths","interface","file_watcher"):
                    for kk,vv in v.items(): sem.set(k,kk,vv)
            sem.save_settings(); return True
        if m=="settings.reset": sem.reset_to_defaults(); return sem.get_all()
        if m=="sessions.getStatus":
            ok=oa.test_connection(); return {"connected":ok,"server":oa.base_url}
        if m=="sessions.testConnection": return oa.test_connection()
        if m=="sessions.getAll": return oa.get_sessions()
        if m=="dialog.selectDir":
            import tkinter as tk
            from tkinter import filedialog
            root=tk.Tk();root.withdraw();root.attributes("-topmost",True)
            init=d.get("dir","")
            if not init or not Path(init).exists(): init=str(Path.home())
            p=filedialog.askdirectory(title=d.get("title",""),initialdir=init)
            root.destroy(); return p or ""
        return {}
    except Exception as e:
        return {"error":str(e)}

dist = BASE / "dist"
if not (dist / "index.html").exists():
    dist = BASE

from http.server import HTTPServer, BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        length=int(self.headers.get("content-length",0))
        body=json.loads(self.rfile.read(length)) if length else {}
        result=dispatch(body.get("method",""),body.get("args",{}))
        b=json.dumps(result,ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_GET(self):
        path=self.path.lstrip("/")
        if not path: path="index.html"
        file=dist/path
        if file.exists() and file.is_file():
            ct={"html":"text/html","js":"application/javascript","css":"text/css","svg":"image/svg+xml","png":"image/png","ico":"image/x-icon"}
            s=file.suffix.lstrip(".")
            self.send_response(200)
            self.send_header("Content-Type",ct.get(s,"application/octet-stream"))
            self.end_headers()
            self.wfile.write(file.read_bytes())
        else:
            self.send_response(200)
            self.send_header("Content-Type","text/html")
            self.end_headers()
            self.wfile.write((dist/"index.html").read_bytes())
    def do_PUT(self):
        self.do_POST()
    def log_message(self,*a): pass

def find_edge():
    for p in [
        Path(os.environ.get("PROGRAMFILES(X86)",""))/"Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES",""))/"Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("LOCALAPPDATA",""))/"Microsoft/Edge/Application/msedge.exe",
    ]:
        if p.exists(): return str(p)
    return "msedge"

def run_server():
    s=socket.socket(); s.bind(("127.0.0.1",0)); port=s.getsockname()[1]; s.close()
    pf=Path(tempfile.gettempdir())/"openclaw_port.txt"
    pf.write_text(str(port))
    HTTPServer(("127.0.0.1",port),H).serve_forever()

def main():
    pf=Path(tempfile.gettempdir())/"openclaw_port.txt"
    pf.unlink(missing_ok=True)

    env=os.environ.copy()
    env["OPENCLAW_SERVER"]="1"
    proc=subprocess.Popen(
        [sys.executable],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0,
        env=env,
    )

    port=8000
    for _ in range(20):
        if pf.exists():
            try: port=int(pf.read_text()); break
            except: pass
        time.sleep(0.3)

    edge=find_edge()
    subprocess.Popen([
        edge,
        f"--app=http://127.0.0.1:{port}",
        "--window-size=1200,800",
        "--disable-gpu",
        "--no-sandbox",
    ])

    proc.wait()

if __name__=="__main__":
    if os.environ.get("OPENCLAW_SERVER"):
        run_server()
    else:
        main()
