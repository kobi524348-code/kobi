import json, urllib.request, urllib.parse, sys
SPEAKER = 3  # ずんだもん（ノーマル）
lines = {
 1: "三日坊主、ありますか？　日記や、ランニング。始めてはみたけれど、続かなかった経験、ありませんか？",
 2: "それって、意志が弱いから？　いいえ、違います。じゃあ、なぜ続かないのでしょう？",
 3: "ロンドン大学の研究によると、習慣になるまでにかかる日数は、平均、ろくじゅうろくにち。人によって、じゅうはちにちから、にひゃくごじゅうよっかまで、大きな差がありました。",
 4: "つまり、三日目は、まだ途中。ここでやめてしまうのは、もったいないんです。",
 5: "コツは、やめられないほど、小さくすること。いちにち、いちぎょう。いちにち、いっぷん。これなら、続けられそうですよね。",
}
base = "http://localhost:50021"
for n, text in lines.items():
    q = urllib.parse.urlencode({"text": text, "speaker": SPEAKER})
    aq = json.load(urllib.request.urlopen(urllib.request.Request(f"{base}/audio_query?{q}", method="POST")))
    aq["speedScale"] = 1.05
    aq["prePhonemeLength"] = 0.3; aq["postPhonemeLength"] = 0.5
    print(n, aq["kana"])
    req = urllib.request.Request(f"{base}/synthesis?speaker={SPEAKER}", data=json.dumps(aq).encode(), headers={"Content-Type": "application/json"})
    open(f"slide{n}.wav", "wb").write(urllib.request.urlopen(req).read())
