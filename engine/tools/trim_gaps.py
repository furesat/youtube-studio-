"""Part mp3'lerdeki uzun sessizlikleri kısaltır (orijinaller audio/<lang>/orig/ altında saklanır).
0.3–0.8 s -> 0.2 s ; >=0.8 s -> 0.5 s. Kullanım: python3 trim_gaps.py videos/001 [--lang tr]"""
import os, sys, shutil, subprocess, re, argparse
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr"); a = ap.parse_args()
d = f"{a.vdir}/audio/{a.lang}"; os.makedirs(d + "/orig", exist_ok=True); SR = 24000
for k in "ABC":
    src = f"{d}/orig/part_{k}.mp3"
    if not os.path.exists(src): shutil.copy(f"{d}/part_{k}.mp3", src)
    raw = subprocess.run(["ffmpeg","-loglevel","error","-i",src,"-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True,check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768
    w = int(0.01*SR); n = len(x)//w
    rms = np.sqrt((x[:n*w].reshape(n,w)**2).mean(1)); db = 20*np.log10(rms+1e-9)
    sil = db < -38; out = []; i = 0; cut = 0
    while i < n:
        if not sil[i]: out.append(x[i*w:(i+1)*w]); i += 1; continue
        j = i
        while j < n and sil[j]: j += 1
        dur = (j-i)*0.01
        if dur >= 0.3 and i > 5 and j < n-5:
            keep = 0.2 if dur < 0.8 else 0.5
            kw = int(keep/0.01); seg = x[i*w:j*w]; half = kw//2
            out.append(np.concatenate([seg[:half*w], seg[-(kw-half)*w:]])); cut += dur-keep
        else: out.append(x[i*w:j*w])
        i = j
    y = np.concatenate(out)
    pcm = (np.clip(y,-1,1)*32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","s16le","-ar",str(SR),"-ac","1","-i","-","-b:a","192k",f"{d}/part_{k}.mp3"],input=pcm,check=True)
    print(k, "kısaltılan sn:", round(cut,2))
