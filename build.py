#!/usr/bin/env python3
"""Assemble les trois pages en un fichier unique, ielts.html.

Chaque page est embarquée telle quelle dans une iframe (srcdoc), ce qui évite
toute collision d'identifiants ou de variables entre les trois applications.
Relancer ce script après chaque modification de index.html, task2.html ou exam.html.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = [
    ("t1", "index.html", "📊 Task 1",  None),
    ("t2", "task2.html", "✍️ Task 2",  None),
    ("co", "exam.html",  "📗 Corrigés", "corrige"),
    ("ex", "exam.html",  "⏱️ Examens", None),
]

def embed(path: pathlib.Path, mode=None) -> str:
    html = path.read_text(encoding="utf-8")
    if mode:
        html = html.replace("<head>", '<head>\n<script>window.IELTS_MODE="%s";</script>' % mode, 1)
    # le sélecteur de pages de l'enfant est masqué : c'est la coque qui le fournit
    html = html.replace("</head>", "<style>.navswitch{display:none!important}</style>\n</head>", 1)
    # échappement pour un littéral de gabarit JS
    html = (html.replace("\\", "\\\\").replace("`", "\\`")
                .replace("${", "\\${").replace("</script>", "<\\/script>"))
    return html

apps = "\n".join(
    "APPS.%s = `%s`;" % (key, embed(ROOT / f, mode)) for key, f, _, mode in PAGES
)
tabs = "\n      ".join(
    '<button class="tab%s" data-k="%s"><span class="ic">%s</span><span>%s</span></button>'
    % (("" if i else " on"), key, *label.split(" ", 1))
    for i, (key, _, label, _m) in enumerate(PAGES)
)

OUT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0f172a">
<title>IELTS Writing — Task 1, Task 2 et examens blancs</title>
<style>
:root{--bg:#0f172a;--card:#1b2744;--card2:#22304f;--txt:#eef2ff;--muted:#9fb0d0;--line:#2e3d60;
  --acc:#6ee7b7;--acc2:#38bdf8}
html[data-theme="light"]{--bg:#f4f7fb;--card:#fff;--card2:#eef3fb;--txt:#12203a;--muted:#5b6b88;
  --line:#dbe4f0;--acc:#0f9d76;--acc2:#0284c7}
*{box-sizing:border-box}
html,body{margin:0;padding:0;height:100%%;overflow:hidden;background:var(--bg)}
body{display:flex;flex-direction:column;height:100dvh;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
#bar{flex:0 0 auto;background:var(--card);border-bottom:2px solid var(--acc2);
  padding:calc(8px + env(safe-area-inset-top,0px)) 8px 8px;display:flex;gap:6px;justify-content:center;align-items:center;
  box-shadow:0 4px 14px rgba(0,0,0,.25);position:relative;z-index:5}
#barlbl{font-weight:800;font-size:14px;color:var(--txt);margin-right:8px;white-space:nowrap}
@media(max-width:560px){#barlbl{display:none}}
.tab{flex:1 1 0;max-width:170px;background:var(--card2);border:2px solid var(--acc2);color:var(--txt);
  font-family:inherit;font-size:11.5px;font-weight:700;padding:5px 2px 6px;border-radius:12px;cursor:pointer;
  display:flex;flex-direction:column;align-items:center;gap:1px;white-space:nowrap;overflow:hidden}
.tab .ic{font-size:17px;line-height:1.15}
.tab.on{background:linear-gradient(135deg,var(--acc),var(--acc2));color:#06202b;border-color:transparent;
  box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 35%%,transparent)}
.tab:not(.on):hover{background:color-mix(in srgb,var(--acc2) 18%%,var(--card2))}
.tab:active{transform:scale(.97)}
#frames{flex:1 1 auto;position:relative;background:var(--bg)}
#frames iframe{position:absolute;inset:0;width:100%%;height:100%%;border:0;display:none;background:var(--bg)}
#frames iframe.on{display:block}
</style>
</head>
<body>
  <nav id="bar">
      <span id="barlbl">IELTS Writing</span>
      %(tabs)s
  </nav>
  <div id="frames"></div>
<script>
"use strict";
const APPS = {};
%(apps)s

const KEYS = {t1:"ielts-t1-v1", t2:"ielts-t2-v1", co:"ielts-corrige-v1", ex:"ielts-exam-v1"};
const frames = document.getElementById("frames");
const made = {};
let current = null;

function show(k){
  if(!made[k]){
    const f = document.createElement("iframe");
    f.setAttribute("allow","clipboard-write");
    f.setAttribute("title", k);
    f.srcdoc = APPS[k];
    frames.appendChild(f);
    made[k] = f;
  }
  Object.keys(made).forEach(function(x){ made[x].classList.toggle("on", x===k); });
  document.querySelectorAll("#bar .tab").forEach(function(b){ b.classList.toggle("on", b.dataset.k===k); });
  current = k;
  try{ localStorage.setItem("ielts-shell-tab", k); }catch(e){}
  syncTheme();
}
document.querySelectorAll("#bar .tab").forEach(function(b){
  b.addEventListener("click", function(){ show(b.dataset.k); });
});

/* la barre suit le thème clair/sombre choisi dans l'application affichée */
function syncTheme(){
  let theme = null;
  try{
    const raw = localStorage.getItem(KEYS[current]);
    if(raw) theme = (JSON.parse(raw)||{}).theme;
  }catch(e){}
  if(!theme) theme = "dark";
  document.documentElement.setAttribute("data-theme", theme);
}
setInterval(syncTheme, 900);

let start = "t1";
try{ const s = localStorage.getItem("ielts-shell-tab"); if(s && APPS[s]) start = s; }catch(e){}
show(start);
</script>
</body>
</html>
""" % {"tabs": tabs, "apps": apps}

(ROOT / "ielts.html").write_text(OUT, encoding="utf-8")
size = (ROOT / "ielts.html").stat().st_size
print("ielts.html écrit — %.0f Ko" % (size/1024))
