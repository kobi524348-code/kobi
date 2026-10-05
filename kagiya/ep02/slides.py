import html, os, subprocess
from script import SCENES
SUB = [("にさんげん","2〜3軒"),("いちいちきゅう番","119番"),("ジャフ","JAF"),("しゃじょう荒らし","車上荒らし"),("しゃけんしょう","車検証"),("、ねんしき","年式"),("なになに","◯◯"),("オーケー","OK"),("三つ","3つ"),("四つ","4つ"),("ひとつめ。","① "),("ふたつめ。","② "),("みっつめ。","③ "),("よっつめ。","④ "),("ひとつ。","① "),("ふたつ。","② "),("みっつ。","③ "),("全部でいくら？を","「全部でいくら？」を"),("その、なんとかして、が","その「なんとかして」が")]
def disp(t):
    for a,b in SUB: t=t.replace(a,b)
    return t
BODY = {
"s1": '<div class="tag">後編</div><div class="c"><div class="h1">鍵が車の中に！</div><div class="h2">焦って<em>「なんとかして」</em>は危ない</div><div class="title">車に鍵を閉じ込めた！【後編】</div></div>',
"s2": '<div class="tag">やってはいけないNG行動</div><div class="c list sm ng"><div><b>✕</b>針金やハンガーで自分で開けようとする<small>ドアの中の配線や部品を壊すと、かえって高くつく</small></div><div><b>✕</b>窓ガラスを割る<small>ガラス交換は鍵開けより高いことが多い（命に関わるときは別）</small></div><div><b>✕</b>ネットでいちばん上の業者にすぐ電話</div></div>',
"s3": '<div class="tag">まずやること</div><div class="c list sm"><div><b>1</b>車内に子ども・ペット → <em>すぐ119番</em></div><div><b>2</b>自動車保険・JAFのロードサービスを確認</div><div><b>3</b>家族が合鍵を持っていないか</div><div class="next">それでもダメなら → 鍵屋に2〜3軒電話</div></div>',
"s4": '<div class="tag">ウラ話</div><div class="c"><div class="h2">車の鍵開けは</div><div class="h1"><em>家より</em>大変</div><div class="note">車種で作りが違う・夜は投光器があっても見にくい</div></div>',
"s5": '<div class="tag">電話で伝える4つのこと</div><div class="c cards c4"><div><b>場所</b>住所・近くの目印</div><div><b>車種・年式</b>だいたいでOK</div><div><b>鍵の種類</b>差し込む鍵？<br>スマートキー？</div><div><b>身分証</b>車検証と<br>一緒に確認</div></div>',
"s6": '<div class="tag">まとめ</div><div class="c list sm"><div><b>1</b>自分で無理に開けない・ガラスを割らない</div><div><b>2</b>子どもやペットが中にいたら、すぐ119番</div><div><b>3</b>保険・JAF・合鍵を確認 → 鍵屋に2〜3軒電話</div><div class="next">次回：夜の鍵開けはなぜ時間がかかる？</div></div>',
}
CSS = """@font-face{font-family:N;src:url(../../narration/thumb/noto900.ttf);font-weight:900}@font-face{font-family:N;src:url(../../narration/thumb/noto700.ttf);font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden}
body{background:#FFF7EC;font-family:N;font-weight:700;color:#3A2E28;position:relative}
.band{position:absolute;top:0;left:0;right:0;height:28px;background:#F08A28}
.ch{position:absolute;right:90px;top:70px;font-size:34px;color:#8A7A70}
.tag{position:absolute;left:90px;top:62px;background:#3A2E28;color:#fff;font-weight:900;font-size:40px;padding:8px 34px;border-radius:40px}
.c{position:absolute;left:0;right:0;top:140px;height:600px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:26px}
.h1{font-weight:900;font-size:140px;line-height:1.1}.h2{font-weight:900;font-size:72px}em{font-style:normal;color:#F08A28}
.title{margin-top:20px;background:#F08A28;color:#fff;font-weight:900;font-size:56px;padding:14px 48px;border-radius:20px}
.note{font-size:48px;color:#6A5A50;background:#fff;border:4px solid #E7D9C4;border-radius:24px;padding:18px 40px}
.ad{font-weight:900;font-size:130px;background:#fff;border:6px solid #E7D9C4;border-radius:30px;padding:10px 60px}
.ring{color:#E04B2A;border:10px solid #E04B2A;border-radius:50%;padding:0 18px;margin-left:10px}
.plus{display:flex;gap:30px}.plus span{font-weight:900;font-size:56px;color:#E04B2A}
.list{align-items:stretch;padding:0 260px;gap:30px}.list>div{text-align:left;font-weight:900;font-size:58px;background:#fff;border:4px solid #E7D9C4;border-radius:28px;padding:22px 40px}
.list b{display:inline-block;width:72px;height:72px;line-height:72px;text-align:center;background:#F08A28;color:#fff;border-radius:50%;margin-right:26px;font-size:46px}
.list small{display:block;font-size:36px;color:#8A7A70;margin:8px 0 0 100px;font-weight:700}
.sm{gap:20px;padding:0 180px}.sm>div{font-size:48px;padding:14px 34px}.sm small{font-size:30px;margin-top:4px}.ng b{background:#E03A1E}.c4{gap:24px}.cards.c4>div{width:340px;height:320px;font-size:36px;padding:20px}.cards.c4 b{font-size:50px}.list .next{background:#3A2E28;color:#fff;border:none;text-align:center;font-size:50px}
.cards{flex-direction:row;gap:40px}.cards>div{width:470px;height:380px;background:#fff;border:6px solid #F08A28;border-radius:36px;display:flex;flex-direction:column;justify-content:center;font-size:44px;padding:30px;line-height:1.4}
.cards b{display:block;font-weight:900;font-size:60px;color:#F08A28;margin-bottom:24px}
.sub{position:absolute;left:70px;right:70px;bottom:50px;min-height:190px;background:rgba(255,255,255,.96);border:6px solid var(--c);border-radius:30px;display:flex;align-items:center;padding:20px 44px;gap:30px}
.who{flex:none;background:var(--c);color:#fff;font-weight:900;font-size:38px;padding:10px 26px;border-radius:20px}
.txt{font-weight:900;font-size:50px;line-height:1.35}"""
os.makedirs("frames",exist_ok=True)
SHELL="/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
for sid, lines in SCENES:
    for i,(who,text) in enumerate(lines):
        c, name = ("#5BAA4A","ずんだもん") if who=="Z" else ("#3B6FB6","元鍵屋")
        h=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="band"></div><div class="ch">鍵屋のウラ話チャンネル</div>{BODY[sid]}<div class="sub" style="--c:{c}"><div class="who">{name}</div><div class="txt" style="font-size:{44 if len(disp(text))>56 else 50}px">{html.escape(disp(text))}</div></div></body></html>'
        open("_f.html","w").write(h)
        subprocess.run([SHELL,"--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files","--window-size=1920,1080","--virtual-time-budget=2000",f"--screenshot={os.getcwd()}/frames/{sid}_{i:02d}.png",f"file://{os.getcwd()}/_f.html"],capture_output=True)
print("done")
