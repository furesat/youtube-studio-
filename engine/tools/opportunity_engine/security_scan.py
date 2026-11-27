"""Read-only, value-redacted scan of text blobs reachable from local Git refs.

No network, no credential validation, no history rewrite. Default output is counts only.
Use --locations locally (never in public CI logs) to locate matched blob IDs.
"""
import argparse
from collections import Counter
import json
import re
import subprocess
import sys

MAX_BYTES=2*1024*1024
PATTERNS={
    "github_token":r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b",
    "google_api_key":r"\bAIza[0-9A-Za-z_-]{35}\b",
    "supabase_secret":r"\bsb_secret_[A-Za-z0-9_-]{25,}\b",
    "jwt_like":r"\beyJ[A-Za-z0-9_-]{12,}\.eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{20,}\b",
    "private_key":r"-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----",
    "aws_key":r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "other_api_key":r"\b(?:sk-proj-|sk-ant-api03-|sk_live_)[A-Za-z0-9_-]{25,}\b",
    "credential_url":r"https?://[^/\s:@]+:[^/\s@]+@(?!(?:example\.(?:test|com|org)|localhost)(?=[:/\s\"']|$))[^/\s]+",
}
# A matched pattern is a candidate, not confirmation of a live secret.
COMPILED={k:re.compile(v) for k,v in PATTERNS.items()}
EMAIL=re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?:com|net|org|at|tr|edu|de|io|co|me|eu|ac)\b",re.I)

def match_types(source):
    hits={kind for kind,p in COMPILED.items() if p.search(source)}
    if any(not re.search(r"example\.(?:com|org|test)|noreply",m.group(),re.I) for m in EMAIL.finditer(source)):
        hits.add("email_shaped")
    return hits

def git(*args,input=None):
    return subprocess.run(["git",*args],input=input,capture_output=True,check=True).stdout

def scan(locations=False):
    current=set()
    for entry in git("ls-tree","-r","-z","HEAD").split(b"\0"):
        if entry:
            meta=entry.split(b"\t",1)[0].split()
            if meta[1]==b"blob":current.add(meta[2].decode("ascii"))
    reachable={line.split(b" ",1)[0].decode("ascii") for line in git("rev-list","--objects","--all","HEAD").splitlines()}
    object_meta=git("cat-file","--batch-check=%(objectname) %(objecttype) %(objectsize)",input=("\n".join(sorted(reachable))+"\n").encode())
    counts=Counter();current_hits=Counter();history_hits=Counter();found=[]
    process=subprocess.Popen(["git","cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    try:
        for line in object_meta.splitlines():
            fields=line.decode("ascii").split()
            if len(fields)!=3:
                counts["unreadable_objects"]+=1;continue
            oid,kind,rawsize=fields
            if kind!="blob":continue
            counts["reachable_blobs"]+=1
            if oid in current:counts["current_blobs"]+=1
            if int(rawsize)>MAX_BYTES:
                counts["oversized_blobs"]+=1
                if oid in current:counts["current_oversized"]+=1
                continue
            process.stdin.write((oid+"\n").encode());process.stdin.flush()
            header=process.stdout.readline().decode("ascii").split()
            if len(header)!=3 or header[0]!=oid or header[1]!="blob":
                raise RuntimeError("Unexpected Git blob response")
            payload=process.stdout.read(int(header[2]))
            if len(payload)!=int(header[2]) or process.stdout.read(1)!=b"\n":raise RuntimeError("Incomplete Git blob response")
            try:
                if b"\0" in payload:raise UnicodeError()
                source=payload.decode("utf-8")
            except UnicodeError:
                counts["binary_or_non_utf8"]+=1
                if oid in current:counts["current_binary_or_non_utf8"]+=1
                continue
            counts["scanned_text_blobs"]+=1
            if oid in current:counts["current_scanned_text_blobs"]+=1
            hits=match_types(source)
            if hits:
                (current_hits if oid in current else history_hits).update(hits)
                if locations:found.append({"blob":oid,"in_head":oid in current,"types":sorted(hits)})
    finally:
        process.stdin.close();process.stdout.close();process.wait()
    if process.returncode:raise RuntimeError("Git blob scan failed")
    metadata=git("log","--all","HEAD","--format=%ae%n%ce").decode("utf-8",errors="replace").splitlines()
    result={"scope":"All blobs reachable from locally available refs and HEAD; UTF-8 <=2 MiB. No unreachable objects, omitted large/binary files, LFS contents, remote-only refs or runtime secrets.","counts":dict(counts),"current_candidate_blobs_by_pattern":dict(current_hits),"historical_only_candidate_blobs_by_pattern":dict(history_hits),"non_noreply_commit_email_fields":sum(bool(v) and "noreply" not in v.lower() for v in metadata),"credential_values_printed":False,"match_confirmation":"manual_review_required"}
    if locations:result["locations"]=found
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locations",action="store_true",help="Local only: show candidate blob IDs, not values")
    parser.add_argument("--fail-current",action="store_true",help="Fail on current credential-shaped candidate, not email-only or historical-only")
    args=parser.parse_args()
    result=scan(args.locations)
    print(json.dumps(result,sort_keys=True,indent=2))
    hits=result["current_candidate_blobs_by_pattern"]
    return int(args.fail_current and any(k!="email_shaped" for k in hits))

if __name__=="__main__":
    sys.exit(main())
