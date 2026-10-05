import html, os, subprocess
from script import SCENES
SUB = [("なになに円から","◯◯円〜"),("にさんげん","2〜3軒"),("にさんぷん","2〜3分"),("一本","1本"),("一万円","1万円"),("三つ","3つ"),("ひとつめ。","① "),("ふたつめ。","② "),("みっつめ。","③ "),("ひとつ。","① "),("ふたつ。","② "),("みっつ。","③ "),("からの部分","「〜」の部分"),("からに注意","「〜」に注意"),("、って","」って"),("鍵開け、◯◯円〜","「鍵開け ◯◯円〜")]
def disp(t):
    for a,b in SUB: t=t.replace(a,b)
    return t
BODY = {
"s1": '<div class="tag">導入</div><div class="c"><div class="h1">鍵をなくした！</div><div class="h2">いちばん上の鍵屋に電話…<em>ちょっと待って！</em></div><div class="title">損しない鍵屋の呼び方【前編】</div></div>',
"s2": '<div class="tag">よくある落とし穴</div><div class="c"><div class="ad">鍵開け 980円<span class="ring">〜</span></div><div class="plus"><span>＋出張費</span><span>＋作業費</span><span>＋夜の割増</span></div><div class="h2">焦っていると、<em>断りにくい</em></div></div>',
"s3": '<div class="tag">ウラ話①</div><div class="c"><div class="h2">見積もりは</div><div class="h1"><em>2〜3軒</em>に電話</div><div class="note">電話1本 2〜3分で、数千円〜1万円以上の差も</div></div>',
"s4": '<div class="tag">電話で聞く3つのこと</div><div class="c list"><div><b>1</b>全部でいくらになりますか？<small>出張費・作業費・夜の料金ぜんぶ込みで</small></div><div><b>2</b>何分くらいで来られますか？</div><div><b>3</b>開かなかったときも、お金はかかりますか？</div></div>',
"s5": '<div class="tag">ウラ話②</div><div class="c"><div class="h2">夜の鍵開けは</div><div class="h1"><em>高く</em>なりやすい</div><div class="note">投光器を使っても、昼より見にくく時間がかかる</div></div>',
"s6": '<div class="tag">呼ぶ前にチェック</div><div class="c cards"><div><b>賃貸なら</b>管理会社・大家さんに連絡</div><div><b>保険・カード</b>鍵開けサービスが付いているかも</div><div><b>身分証明書</b>確認する鍵屋は安心</div></div>',
"s7": '<div class="tag">まとめ</div><div class="c list sm"><div><b>1</b>「◯◯円〜」の広告は「〜」に注意</div><div><b>2</b>2〜3軒に電話して「全部でいくら？」を比べる</div><div><b>3</b>呼ぶ前に 管理会社・保険・身分証をチェック</div><div class="next">後編：車に鍵を閉じ込めたら？</div></div>',
}
CSS = """@font-face{font-family:N;src:url(../../narration/thumb/noto900.ttf);font-weight:900}@font-face{font-family:N;src:url(../../narration/thumb/noto700.ttf);font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden}
body{background:#FFF7EC;font-family:N;font-weight:700;color:#3A2E28;position:relative}
.band{position:absolute;top:0;left:0;right:0;height:28px;background:#F08A28}
.ch{position:absolute;right:90px;top:70px;font-size:34px;color:#8A7A70}
.tag{position:absolute;left:90px;top:62px;background:#3A2E28;color:#fff;font-weight:900;font-size:40px;padding:8px 34px;border-radius:40px}
.c{position:absolute;left:0;right:0;top:170px;height:610px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:26px}
.h1{font-weight:900;font-size:140px;line-height:1.1}.h2{font-weight:900;font-size:72px}em{font-style:normal;color:#F08A28}
.title{margin-top:20px;background:#F08A28;color:#fff;font-weight:900;font-size:56px;padding:14px 48px;border-radius:20px}
.note{font-size:48px;color:#6A5A50;background:#fff;border:4px solid #E7D9C4;border-radius:24px;padding:18px 40px}
.ad{font-weight:900;font-size:130px;background:#fff;border:6px solid #E7D9C4;border-radius:30px;padding:10px 60px}
.ring{color:#E04B2A;border:10px solid #E04B2A;border-radius:50%;padding:0 18px;margin-left:10px}
.plus{display:flex;gap:30px}.plus span{font-weight:900;font-size:56px;color:#E04B2A}
.list{align-items:stretch;padding:0 260px;gap:30px}.list>div{text-align:left;font-weight:900;font-size:58px;background:#fff;border:4px solid #E7D9C4;border-radius:28px;padding:22px 40px}
.list b{display:inline-block;width:72px;height:72px;line-height:72px;text-align:center;background:#F08A28;color:#fff;border-radius:50%;margin-right:26px;font-size:46px}
.list small{display:block;font-size:36px;color:#8A7A70;margin:8px 0 0 100px;font-weight:700}
.sm{gap:20px;padding:0 220px}.sm>div{font-size:50px;padding:16px 36px}.list .next{background:#3A2E28;color:#fff;border:none;text-align:center;font-size:50px}
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
        h=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="band"></div><div class="ch">鍵屋のウラ話チャンネル</div>{BODY[sid]}<div class="sub" style="--c:{c}"><div class="who">{name}</div><div class="txt">{html.escape(disp(text))}</div></div></body></html>'
        open("_f.html","w").write(h)
        subprocess.run([SHELL,"--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files","--window-size=1920,1080","--virtual-time-budget=2000",f"--screenshot={os.getcwd()}/frames/{sid}_{i:02d}.png",f"file://{os.getcwd()}/_f.html"],capture_output=True)
print("done")
