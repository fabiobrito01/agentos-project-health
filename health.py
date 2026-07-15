"""Auditoria rápida e sem dependências para repositórios de software."""
import argparse, json
from pathlib import Path
RULES={"README":lambda p:any(p.glob("README*")),"LICENSE":lambda p:any(p.glob("LICENSE*")),"Gitignore":lambda p:(p/".gitignore").exists(),"CI":lambda p:(p/".github/workflows").exists(),"Testes":lambda p:any((p/x).exists() for x in ("tests","test","__tests__"))}
def scan(path):
 p=Path(path); checks={k:bool(f(p)) for k,f in RULES.items()}; score=round(sum(checks.values())/len(checks)*100); return {"project":p.name,"score":score,"checks":checks}
def main(argv=None):
 ap=argparse.ArgumentParser(); ap.add_argument("path",nargs="?",default="."); ap.add_argument("--json",action="store_true"); a=ap.parse_args(argv); r=scan(a.path)
 if a.json: print(json.dumps(r,ensure_ascii=False,indent=2))
 else:
  print(f"AgentOS Project Health · {r['project']} · {r['score']}/100"); [print(f"{'✓' if ok else '✗'} {name}") for name,ok in r['checks'].items()]
if __name__=="__main__": main()
