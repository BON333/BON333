#!/usr/bin/env python3
"""Gera o cartão 'Year of the Eclipse' (SVG animado) para o README do perfil."""
import base64, collections, json, os, random, subprocess, sys

portrait_path, out_path = sys.argv[1], sys.argv[2]
portrait = base64.b64encode(open(portrait_path, "rb").read()).decode()
LOGIN = "BON333"

# --- dados reais (gh CLI; no Actions usa GH_TOKEN) ---
QUERY = """{user(login:"%s"){name location createdAt followers{totalCount}
repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount}
prOpen:pullRequests(states:OPEN){totalCount} prMerged:pullRequests(states:MERGED){totalCount}
issOpen:issues(states:OPEN){totalCount} issClosed:issues(states:CLOSED){totalCount}
contributionsCollection{totalCommitContributions contributionCalendar{totalContributions
weeks{contributionDays{contributionCount}}}}
repos:repositories(first:100,ownerAffiliations:OWNER,isFork:false){nodes{
languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}}}""" % LOGIN
u = json.loads(subprocess.check_output(["gh", "api", "graphql", "-f", f"query={QUERY}"]))["data"]["user"]
langs = collections.Counter()
for r in u["repos"]["nodes"]:
    for e in r["languages"]["edges"]:
        langs[e["node"]["name"]] += e["size"]
top = langs.most_common(3)
cal = u["contributionsCollection"]["contributionCalendar"]
days = [d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]]

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

W, H = 1024, 560
FONT = "'VT323',monospace"
TITLE = "'Press Start 2P',monospace"
PX = 3  # tamanho do "pixel" da arte
FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")

def font_face(name, file):
    data = base64.b64encode(open(os.path.join(FONTS_DIR, file), "rb").read()).decode()
    return f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{data}) format('woff2')}}"
PARCH, INK, BLOOD, GOLD = "#cdb894", "#2b1d14", "#8e1414", "#e3c49a"
CYCLE = 14  # segundos por ciclo dos terminais

art, txt = [], []

def a(s):
    # texto e retrato ficam fora do filtro de pixelização
    (txt if s.startswith(('<text', '<image')) else art).append(s)

head = (f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" shape-rendering="crispEdges">
<title>BON333 — Year of the Eclipse</title>
<style>
{font_face("VT323", "VT323.woff2")}
{font_face("Press Start 2P", "PressStart2P.woff2")}
text{{font-weight:normal}}
.t{{font-family:{TITLE}}}
.flame{{transform-box:fill-box;transform-origin:50% 100%;animation:flick .35s ease-in-out infinite alternate}}
.flame2{{animation-duration:.5s;animation-delay:.1s}}
@keyframes flick{{0%{{transform:scale(1,1) skewX(0)}}50%{{transform:scale(.9,1.12) skewX(4deg)}}100%{{transform:scale(1.05,.92) skewX(-3deg)}}}}
.glow{{animation:glow 1.2s ease-in-out infinite alternate}}
@keyframes glow{{from{{opacity:.35}}to{{opacity:.7}}}}
.pulse{{animation:pulse 3s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:0}}50%{{opacity:.6}}}}
.brand{{animation:brand 2.6s ease-in-out infinite}}
@keyframes brand{{0%,100%{{opacity:.85}}50%{{opacity:1;filter:drop-shadow(0 0 6px #ff2a2a)}}}}
.needle{{transform-origin:579px 362px;animation:needle 4s ease-in-out infinite}}
@keyframes needle{{0%,100%{{transform:rotate(-20deg)}}40%{{transform:rotate(55deg)}}55%{{transform:rotate(45deg)}}70%{{transform:rotate(62deg)}}}}
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.drip{{animation:drip 5s ease-in infinite}}
@keyframes drip{{0%,60%{{transform:translateY(0);opacity:1}}100%{{transform:translateY(14px);opacity:0}}}}
</style>
<defs>
<filter id="px" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
  <feFlood x="{PX//2}" y="{PX//2}" width="1" height="1" flood-color="#000"/>
  <feComposite width="{PX}" height="{PX}"/>
  <feTile result="grid"/>
  <feComposite in="SourceGraphic" in2="grid" operator="in"/>
  <feMorphology operator="dilate" radius="{PX//2}"/>
</filter>
<pattern id="bricks" width="64" height="32" patternUnits="userSpaceOnUse">
  <rect width="64" height="32" fill="#2b2826"/>
  <rect x="1" y="1" width="62" height="14" fill="#353130"/>
  <rect x="-31" y="17" width="62" height="14" fill="#312d2b"/>
  <rect x="33" y="17" width="62" height="14" fill="#383432"/>
  <rect x="4" y="3" width="10" height="2" fill="#403b38"/>
  <rect x="40" y="21" width="8" height="2" fill="#403b38"/>
</pattern>
<pattern id="grain" width="6" height="6" patternUnits="userSpaceOnUse">
  <rect width="6" height="6" fill="{PARCH}"/>
  <rect x="1" y="2" width="1" height="1" fill="#bfa982"/>
  <rect x="4" y="4" width="1" height="1" fill="#d8c6a3"/>
</pattern>
<radialGradient id="vignette" cx="50%" cy="45%" r="65%">
  <stop offset="60%" stop-color="#000" stop-opacity="0"/>
  <stop offset="100%" stop-color="#000" stop-opacity=".75"/>
</radialGradient>
<radialGradient id="torchlight" r="50%">
  <stop offset="0%" stop-color="#ff8a2a" stop-opacity=".55"/>
  <stop offset="100%" stop-color="#ff5a00" stop-opacity="0"/>
</radialGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#4a4340"/><stop offset="1" stop-color="#231f1d"/>
</linearGradient>
<linearGradient id="gauge" x1="0" x2="1">
  <stop offset="0" stop-color="#3d6b2a"/><stop offset=".5" stop-color="#b5891f"/><stop offset="1" stop-color="#a31515"/>
</linearGradient>
<symbol id="skull" viewBox="0 0 20 22">
  <path d="M10 1C4.5 1 1 4.6 1 9.5c0 3 1.3 5 3.5 6.2V20h11v-4.3C17.7 14.5 19 12.5 19 9.5 19 4.6 15.5 1 10 1z" fill="#d9cfbd" stroke="#1a1412" stroke-width="1"/>
  <ellipse cx="6.5" cy="10" rx="2.6" ry="2.8" fill="#1a1412"/>
  <ellipse cx="13.5" cy="10" rx="2.6" ry="2.8" fill="#1a1412"/>
  <path d="M10 13l-1.4 2.6h2.8z" fill="#1a1412"/>
  <path d="M7.5 17v3M10 17v3M12.5 17v3" stroke="#1a1412" stroke-width=".8"/>
</symbol>
<symbol id="brandmark" viewBox="-30 -50 60 100">
  <g fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="square">
    <path d="M0 -44V44"/>
    <path d="M0 -18L-20 -42M0 -18L20 -42"/>
    <path d="M0 18L-20 42M0 18L20 42"/>
    <path d="M-18 -6C-6 -14 6 2 18 -6" stroke-width="6"/>
  </g>
</symbol>
<symbol id="horn" viewBox="0 0 40 30">
  <path d="M38 28C30 26 18 22 10 12 6 7 4 3 2 1c4 3 10 6 16 8 8 3 14 8 20 19z" fill="#cfc4ae" stroke="#1a1412" stroke-width="1.2"/>
</symbol>
<clipPath id="pclip"><rect x="437" y="96" width="148" height="146"/></clipPath>
</defs>
''')

# --- fundo ---
a(f'<rect width="{W}" height="{H}" fill="url(#bricks)"/>')

def torch(x, y):
    a(f'<circle class="glow" cx="{x}" cy="{y-10}" r="70" fill="url(#torchlight)"/>')
    a(f'<path d="M{x-14} {y}h28l-6 10h-16z" fill="#3a2f28" stroke="#120e0c" stroke-width="2"/>')
    a(f'<rect x="{x-4}" y="{y+10}" width="8" height="46" fill="#4a3a2c" stroke="#120e0c" stroke-width="2"/>')
    a(f'<path class="flame" d="M{x} {y-40}c10 12 14 22 10 32 -2 6 -18 6 -20 0 -4-10 0-20 10-32z" fill="#ff6a00"/>')
    a(f'<path class="flame flame2" d="M{x} {y-26}c6 8 8 14 5 20 -2 4-8 4-10 0 -3-6-1-12 5-20z" fill="#ffd34d"/>')

torch(28, 160); torch(996, 160)

def sigil(x, y, s=40):
    a(f'<use href="#brandmark" xlink:href="#brandmark" x="{x-s/2}" y="{y-s*0.8}" width="{s}" height="{s*1.6}" color="#6e1010" opacity=".8"/>')
for x, y in [(996, 34), (996, 525), (28, 525)]:
    sigil(x, y, 26)
for x, y in [(30, 330), (995, 330)]:
    a(f'<use href="#skull" xlink:href="#skull" x="{x-16}" y="{y}" width="32" height="35" opacity=".55"/>')

# --- moldura principal ---
a('<rect x="52" y="34" width="920" height="492" rx="6" fill="#262220" stroke="#0e0b0a" stroke-width="4"/>')
a('<rect x="58" y="40" width="908" height="480" rx="4" fill="none" stroke="#4a4240" stroke-width="2"/>')
for x, y in [(52, 34), (972, 34), (52, 526), (972, 526)]:
    a(f'<circle cx="{x}" cy="{y}" r="9" fill="url(#metal)" stroke="#0e0b0a" stroke-width="2"/>')
# salpicos de sangue
random.seed(1997)
for _ in range(26):
    x, y = random.choice([(random.randint(60, 380), random.randint(500, 525)),
                          (random.randint(640, 965), random.randint(500, 525)),
                          (random.randint(60, 90), random.randint(60, 500)),
                          (random.randint(940, 965), random.randint(60, 500))])
    a(f'<circle cx="{x}" cy="{y}" r="{random.uniform(1.2, 3.5):.1f}" fill="{BLOOD}" opacity=".75"/>')

# --- topo ---
a(f'<rect x="88" y="46" width="318" height="9" fill="{BLOOD}" stroke="#0e0b0a" stroke-width="2"/>')
a(f'<rect x="620" y="46" width="318" height="9" fill="{BLOOD}" stroke="#0e0b0a" stroke-width="2"/>')
a('<rect x="944" y="40" width="18" height="18" fill="#5a1010" stroke="#0e0b0a" stroke-width="2"/><path d="M948 44l10 10M958 44l-10 10" stroke="#d9cfbd" stroke-width="2"/>')
a('<use href="#horn" xlink:href="#horn" x="376" y="18" width="42" height="32"/>')
a('<use href="#horn" xlink:href="#horn" x="606" y="18" width="42" height="32" transform="translate(1254 0) scale(-1 1)"/>')
a('<rect x="412" y="28" width="200" height="54" fill="#1c1816" stroke="#0e0b0a" stroke-width="3"/>')
a('<rect x="418" y="34" width="188" height="42" fill="none" stroke="#5a4e48" stroke-width="2"/>')
a('<use href="#skull" xlink:href="#skull" x="500" y="2" width="24" height="26"/>')
a(f'<text x="512" y="64" text-anchor="middle" class="t" font-size="24" fill="{GOLD}">BON333</text>')

def heading(x, y, text):
    a(f'<path d="M{x} {y-9}l6 6 6-6z" fill="{BLOOD}"/>')
    a(f'<text x="{x+18}" y="{y}" class="t" font-size="8" fill="{GOLD}">{text}</text>')

def parch(x, y, w, h):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#grain)" stroke="#1a1412" stroke-width="3"/>')
    a(f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" fill="none" stroke="#a8936e" stroke-width="1"/>')

# --- user overview ---
heading(86, 88, "USER OVERVIEW")
parch(86, 96, 278, 118)
rows = [("User:", LOGIN), ("Real Name:", esc((u["name"] or LOGIN).strip())),
        ("Repositories:", u["repositories"]["totalCount"]), ("Followers:", u["followers"]["totalCount"]),
        ("Joined:", "Year " + u["createdAt"][:4]), ("Location:", esc(u["location"] or "Unknown"))]
for i, (k, v) in enumerate(rows):
    a(f'<text x="98" y="{116+i*17.5:.1f}" font-size="16" fill="{INK}" xml:space="preserve">{k:<14}<tspan fill="#4a1010">{v}</tspan></text>')

# --- terminais ---
def terminal(x, y, w, h, lines, offset, title=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0b0909" stroke="#3a3330" stroke-width="3"/>')
    ty = y + 22
    if title:
        a(f'<rect x="{x}" y="{y}" width="{w}" height="18" fill="#3a3533"/>')
        a(f'<text x="{x+8}" y="{y+13}" font-size="16" fill="#d9cfbd">{title}</text>')
        for i, g in enumerate("_□×"):
            a(f'<text x="{x+w-46+i*14}" y="{y+13}" font-size="16" fill="#d9cfbd">{g}</text>')
        ty = y + 38
    n = len(lines)
    for i, segs in enumerate(lines):
        ly = ty + i * 16.5
        cid = f"tc{offset}_{i}"
        start = (offset + i * 1.6) / CYCLE
        end = min(start + 1.2 / CYCLE, 0.92)
        lw = w - 10
        a(f'<clipPath id="{cid}"><rect x="{x+5}" y="{ly-12}" height="16" width="{lw}">'
          f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" '
          f'keyTimes="0;{";".join(f"{start+(end-start)*k/24:.4f}" for k in range(25))};0.97" '
          f'values="0;{";".join(f"{lw*k/24:.1f}" for k in range(25))};0"/></rect></clipPath>')
        body = "".join(f'<tspan fill="{c}">{t}</tspan>' for t, c in segs)
        a(f'<text x="{x+6}" y="{ly}" font-size="14" fill="#e9e2d6" clip-path="url(#{cid})" xml:space="preserve">&gt; {body}</text>')
    cy = ty + n * 16.5
    a(f'<rect class="blink" x="{x+10}" y="{cy-11}" width="8" height="13" fill="#e9e2d6"/>')

W_ = "#e9e2d6"; R = "#e04040"; P = "#e07a9a"
terminal(78, 246, 290, 132, [
    [("Initiating... Protocol ", W_), ("[ECLIPSE]", R)],
    [("Analyzing codebase... ", W_), ("PURE detected.", P)],
    [("Analyzing codebase... ", W_), ("PURE detected.", P)],
    [("Memory leak in ", W_), ("[BEHELIT.cpp]", R), (" at line 124", W_)],
    [("Searching for ", W_), ("[GRIFFITH]", R), ("... ", W_), ("[FOUND-ACTIVATING]", R)],
    [("Committing 'Dream of Falconia' to repo: ", W_), ("[FATE]", R)],
], 0)
# osso + caveira sobre o terminal
a('<rect x="70" y="233" width="306" height="9" rx="4" fill="#d9cfbd" stroke="#1a1412" stroke-width="2"/>')
a('<use href="#skull" xlink:href="#skull" x="206" y="216" width="32" height="35"/>')

terminal(78, 390, 290, 124, [
    [("Initiating... Protocol ", W_), ("[ECLIPSE]", R)],
    [("Analyzing codebase... ", W_), ("PURE", P), (" detected.", W_)],
    [("Memory leak in ", W_), ("[BEHELIT.cpp]", R), (" at line 124", W_)],
    [("Searching for ", W_), ("[GRIFFITH]", R), ("... ", W_), ("[FOUND]", R)],
    [("Committing 'Apostle integrations' to repo:", W_)],
], 4, title="TERMINAL LOG")

# --- retrato ---
a('<rect x="424" y="84" width="174" height="172" fill="#1c1816" stroke="#0e0b0a" stroke-width="4"/>')
a('<rect x="431" y="90" width="160" height="158" fill="#3a1010" stroke="#6a5a50" stroke-width="2"/>')
a(f'<image x="437" y="96" width="148" height="146" clip-path="url(#pclip)" style="image-rendering:pixelated" '
  f'href="data:image/png;base64,{portrait}" xlink:href="data:image/png;base64,{portrait}"/>')
for x in (398, 626):
    a(f'<path d="M{x} 110l14 14v100l-14 14-14-14V124z" fill="#2a2321" stroke="#0e0b0a" stroke-width="2"/>')
    a(f'<use href="#brandmark" xlink:href="#brandmark" x="{x-10}" y="148" width="20" height="34" color="{BLOOD}"/>')
a('<use href="#skull" xlink:href="#skull" x="384" y="154" width="28" height="31" opacity=".85"/>')
a(f'<text x="512" y="280" text-anchor="middle" class="t" font-size="16" fill="{GOLD}">BON333</text>')

# --- linguagens ---
parch(380, 288, 128, 92)
a(f'<text x="388" y="304" font-size="16" fill="{INK}">LANGUAGES:</text>')
a(f'<text x="388" y="318" font-size="13" fill="{INK}">{" / ".join(esc(n.upper()) for n, _ in top)}</text>')
for i, (fill, (_, size)) in enumerate(zip(["#a31515", "#8a8480", "#6a1414"], top)):
    h = max(8, round(44 * size / top[0][1]))
    x = 392 + i * 24
    a(f'<rect x="{x}" y="326" width="18" height="46" fill="#1a1412"/>')
    a(f'<rect x="{x+2}" y="{372-h}" width="14" height="{h-2}" fill="{fill}">'
      f'<animate attributeName="height" values="{h-2};{h*0.6:.0f};{h-2}" dur="{3+i}s" repeatCount="indefinite"/>'
      f'<animate attributeName="y" values="{372-h};{372-h*0.6-2:.0f};{372-h}" dur="{3+i}s" repeatCount="indefinite"/></rect>')
# elmo
a('<path d="M472 360c0-14 6-22 14-22s14 8 14 22h-6v-6h-16v6z" fill="#3a3533" stroke="#0e0b0a" stroke-width="2"/>'
  '<rect x="478" y="348" width="16" height="3" fill="#0e0b0a"/>')

# --- complexidade ---
parch(514, 288, 130, 92)
a(f'<text x="522" y="304" font-size="16" fill="{INK}">CODE COMPLEXITY:</text>')
a(f'<text x="522" y="318" font-size="16" fill="{BLOOD}">HIGH</text>')
a('<path d="M541 362a38 38 0 0 1 76 0" fill="none" stroke="#1a1412" stroke-width="14"/>')
a('<path d="M541 362a38 38 0 0 1 76 0" fill="none" stroke="url(#gauge)" stroke-width="9"/>')
a('<g class="needle"><path d="M579 362l-2-34h4z" fill="#d9cfbd" stroke="#1a1412"/></g><circle cx="579" cy="362" r="4" fill="#1a1412"/>')
a(f'<text x="579" y="376" text-anchor="middle" font-size="15" fill="{BLOOD}">CURSED</text>')

# --- barras de estatísticas ---
def stat(y, h, label, value):
    parch(380, y, 264, h)
    a(f'<text x="504" y="{y+15}" font-size="16" fill="{INK}">{label}</text>')
    a(f'<text x="504" y="{y+29}" font-size="16" fill="{INK}">{value}</text>')

stat(386, 36, "COMMITS (ÚLTIMO ANO):", u["contributionsCollection"]["totalCommitContributions"])
for i in range(5):
    a(f'<use href="#skull" xlink:href="#skull" x="{388+i*22}" y="{391}" width="22" height="25"/>')
stat(428, 38, "PULL REQUESTS:", f'{u["prOpen"]["totalCount"]} open / {u["prMerged"]["totalCount"]} merged')
for i in range(5):
    a(f'<rect x="{388+i*21}" y="{441 if i % 2 else 438}" width="26" height="{12 if i % 2 else 18}" rx="6" fill="none" stroke="#3a3533" stroke-width="4"/>')
stat(472, 40, "ISSUES:", f'{u["issOpen"]["totalCount"]} open / {u["issClosed"]["totalCount"]} closed')
a(f'<path d="M418 478c8 0 12 6 12 14s-5 14-12 14-12-6-12-14 4-14 12-14z" fill="{BLOOD}" stroke="#1a1412" stroke-width="2"/>'
  '<circle cx="414" cy="488" r="2" fill="#1a1412"/><circle cx="422" cy="488" r="2" fill="#1a1412"/>')

# --- contribuições ---
heading(656, 88, "CONTRIBUTIONS - YEAR OF THE ECLIPSE")
parch(652, 96, 300, 420)
a(f'<text x="810" y="118" text-anchor="middle" font-size="17" fill="{INK}">Days/Weeks</text>')
a(f'<text x="810" y="508" text-anchor="middle" font-size="17" fill="{INK}">{cal["totalContributions"]} contributions no último ano</text>')
GX, GY, CW, CH, N = 688, 144, 18, 23, 14
for c in range(N):
    a(f'<text x="{GX+c*CW+CW/2}" y="{GY-6}" text-anchor="middle" font-size="15" fill="{INK}">{c}</text>')
    a(f'<text x="{GX+c*CW+CW/2}" y="{GY+N*CH+13}" text-anchor="middle" font-size="15" fill="{INK}">{c}</text>')
for r in range(N):
    a(f'<text x="{GX-6}" y="{GY+r*CH+CH/2+4}" text-anchor="end" font-size="15" fill="{INK}">{r+1}</text>')
a(f'<rect x="{GX-2}" y="{GY-2}" width="{N*CW+4}" height="{N*CH+4}" fill="#1a0606"/>')
shades = ["#4f1010", "#5e1212", "#741515", "#8c1919", "#a81e1e", "#c62626"]
# últimos 196 dias, 14 por linha (duas semanas por linha)
recent = ([0] * N * N + days)[-N * N:]
peak = max(recent) or 1
random.seed(333)
for r in range(N):
    for c in range(N):
        x, y = GX + c * CW, GY + r * CH
        n = recent[r * N + c]
        s = shades[0] if n == 0 else shades[min(5, 2 + round(3 * n / peak))]
        a(f'<rect x="{x+1}" y="{y+1}" width="{CW-2}" height="{CH-2}" fill="{s}"/>')
        if n:
            d = random.uniform(0, 3)
            a(f'<rect class="pulse" style="animation-delay:{d:.2f}s" x="{x+1}" y="{y+1}" width="{CW-2}" height="{CH-2}" fill="#e02a2a"/>')
# marca do sacrifício
bx, by = GX + N * CW / 2, GY + N * CH / 2
a(f'<rect x="{bx-26}" y="{by-58}" width="52" height="116" rx="8" fill="#0b0909" opacity=".8"/>')
a(f'<g class="brand"><use href="#brandmark" xlink:href="#brandmark" x="{bx-30}" y="{by-50}" width="60" height="100" color="#e01818"/></g>')
a(f'<rect x="{bx-102}" y="{by-22}" width="72" height="40" fill="#0b0909" opacity=".85"/>')
a(f'<text x="{bx-66}" y="{by-5}" text-anchor="middle" font-size="17" fill="#e9e2d6">BRAND OF</text>')
a(f'<text x="{bx-66}" y="{by+11}" text-anchor="middle" font-size="17" fill="#e9e2d6">sacrifice</text>')
# behelit
a(f'<path d="M676 112c8 0 12 6 12 14s-5 14-12 14-12-6-12-14 4-14 12-14z" fill="{BLOOD}" stroke="#1a1412" stroke-width="2"/>'
  '<circle cx="672" cy="122" r="2" fill="#1a1412"/><circle cx="680" cy="122" r="2" fill="#1a1412"/><path d="M671 131q5 3 10 0" stroke="#1a1412" fill="none"/>')

# --- rodapé ---
a('<use href="#horn" xlink:href="#horn" x="470" y="512" width="34" height="26"/>')
a('<use href="#horn" xlink:href="#horn" x="520" y="512" width="34" height="26" transform="translate(1074 0) scale(-1 1)"/>')
a('<use href="#skull" xlink:href="#skull" x="496" y="514" width="32" height="35"/>')
for x in (140, 300, 720, 880):
    a(f'<circle class="drip" style="animation-delay:{x%5}s" cx="{x}" cy="528" r="2.5" fill="{BLOOD}"/>')

a(f'<rect width="{W}" height="{H}" fill="url(#vignette)" pointer-events="none"/>')
open(out_path, "w", encoding="utf-8").write("\n".join(
    [head, '<g filter="url(#px)">', *art, '</g>', '<g text-rendering="optimizeSpeed">', *txt, '</g>', '</svg>']))
