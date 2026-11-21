#!/usr/bin/env python3
"""Small local CLI for validating briefs, scripts, claims, assets and QA."""
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from fonsisnet_sdd.core import *

def main():
 p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
 for cmd in ('brief','script','claims','asset','audio','qa'):
  q=sub.add_parser(cmd); q.add_argument('file')
  if cmd in ('asset','audio'): q.add_argument('--evidence-dir', type=Path, default=None)
 a=p.parse_args(); data=load_json(a.file)
 if a.cmd=='brief': result=validate_brief(data)
 elif a.cmd=='script': result=validate_script(data)
 elif a.cmd=='claims': result=check_claims(data)
 elif a.cmd=='asset': result=register_asset(data, a.evidence_dir)
 elif a.cmd=='audio': result=validate_audio_package(data, a.evidence_dir)
 else: result=qa_checklist(data)
 print(json.dumps(result,ensure_ascii=False,indent=2));
 if isinstance(result,list) and result: raise SystemExit(1)
 if isinstance(result,dict) and result.get('passed') is False: raise SystemExit(1)
if __name__=='__main__': main()
