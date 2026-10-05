import json, urllib.request, urllib.parse, os
from script import SCENES, SPEAKERS
B="http://localhost:50021"; os.makedirs("wav",exist_ok=True)
for sid, lines in SCENES:
    for i,(who,text) in enumerate(lines):
        sp=SPEAKERS[who]
        q=urllib.parse.urlencode({"text":text,"speaker":sp})
        aq=json.load(urllib.request.urlopen(urllib.request.Request(f"{B}/audio_query?{q}",method="POST")))
        aq["speedScale"]=1.1 if who=="Z" else 1.05
        aq["prePhonemeLength"]=0.05; aq["postPhonemeLength"]=0.25
        print(sid,i,who,aq["kana"])
        r=urllib.request.Request(f"{B}/synthesis?speaker={sp}",data=json.dumps(aq).encode(),headers={"Content-Type":"application/json"})
        open(f"wav/{sid}_{i:02d}.wav","wb").write(urllib.request.urlopen(r).read())
