#!/usr/bin/env python3
"""
Build vertical 1080x1920 slide deck.
PACKED: minimal padding, tight spacing, content fills the frame.
"""
import re, html, os

def ct(t):
    t = html.unescape(t)
    t = re.sub(r'<[^>]+>', '', t)
    return t.strip()

def extract_items(sec):
    items = []
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', sec, re.DOTALL):
        t = ct(m.group(1))
        if t: items.append(('h2', t))
    for m in re.finditer(r'<h4[^>]*>(.*?)</h4>', sec, re.DOTALL):
        t = ct(m.group(1))
        if t: items.append(('h3', t))
    for m in re.finditer(r'<h5[^>]*>(.*?)</h5>', sec, re.DOTALL):
        t = ct(m.group(1))
        if t: items.append(('h4', t))
    for m in re.finditer(r'<div class="content-text">(.*?)</div>', sec, re.DOTALL):
        t = ct(m.group(1))
        if t: items.append(('p', t))
    for m in re.finditer(r'<li[^>]*>(.*?)</li>', sec, re.DOTALL):
        t = ct(m.group(1))
        if t: items.append(('li', t))
    for m in re.finditer(r'<table[^>]*>(.*?)</table>', sec, re.DOTALL):
        rows = []
        for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', m.group(0), re.DOTALL):
            cells = [ct(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', tr.group(1), re.DOTALL)]
            if cells: rows.append(cells)
        if rows: items.append(('table', rows))
    for m in re.finditer(r'<div class="(callout[^"]*)">(.*?)</div>\s*</div>', sec, re.DOTALL):
        cls = m.group(1)
        t = ct(m.group(2))
        if t:
            k = 'pearl' if 'pearl' in cls else 'warn' if 'warn' in cls else 'danger' if 'danger' in cls else 'note'
            items.append((k, t))
    for m in re.finditer(r'<div class="stat-card">(.*?)</div>\s*</div>', sec, re.DOTALL):
        t = ct(m.group(1))
        if t: items.append(('stat', t))
    return items

def est_h(item):
    k = item[0]
    if k == 'h2': return 44
    if k == 'h3': return 38
    if k == 'h4': return 34
    if k == 'p': return max(24, (len(item[1]) // 65 + 1) * 24 + 8)
    if k == 'li': return max(22, (len(item[1]) // 65 + 1) * 24 + 4)
    if k == 'table': return len(item[1]) * 36 + 12
    if k in ('pearl','warn','danger','note'): return max(30, (len(item[1]) // 60 + 1) * 24 + 20)
    if k == 'stat': return 38
    return 24

def render(item):
    k = item[0]
    if k == 'h2': return '<div class="sh">'+item[1]+'</div>'
    if k == 'h3': return '<div class="sh2">'+item[1]+'</div>'
    if k == 'h4': return '<div class="sh3">'+item[1]+'</div>'
    if k == 'p': return '<div class="pt">'+item[1]+'</div>'
    if k == 'li': return '<div class="bl">'+item[1]+'</div>'
    if k == 'table':
        rows = item[1]
        h = ''
        for i,r in enumerate(rows):
            cs = ''.join(('<th>' if i==0 else '<td>') + c + ('</th>' if i==0 else '</td>') for c in r)
            h += '<tr>'+cs+'</tr>'
        return '<table class="tb">'+h+'</table>'
    if k == 'pearl': return '<div class="cp">'+item[1]+'</div>'
    if k == 'warn': return '<div class="cw">'+item[1]+'</div>'
    if k == 'danger': return '<div class="cd">'+item[1]+'</div>'
    if k == 'note': return '<div class="cn">'+item[1]+'</div>'
    if k == 'stat': return '<div class="cs">'+item[1]+'</div>'
    return ''

def pack(items, ttitle, tcolor, tnum, ttotal):
    USABLE = 1810  # 1920 - 50(header) - 30(top pad) - 30(bottom pad)
    slides = []
    buf, bh = [], 0
    for it in items:
        h = est_h(it)
        if bh + h > USABLE and buf:
            slides.append(buf)
            buf, bh = [it], h
        else:
            buf.append(it)
            bh += h
    if buf: slides.append(buf)
    
    out = []
    for si, sitems in enumerate(slides):
        ch = '\n'.join(render(it) for it in sitems)
        nc = sum(len(it[1]) if isinstance(it[1], str) else sum(len(c) for r in it[1] for c in r) for it in sitems)
        sp = 'co' if len(sitems) > 10 or nc > 1500 else ''
        out.append(
            '<div class="sl" data-n="__N__">'
            '<div class="sb '+sp+'">'
            '<div class="hd" style="border-color:'+tcolor+'">'
            '<span class="hn" style="background:'+tcolor+'">'+str(tnum)+'</span>'
            '<span class="ht">'+ttitle+'</span>'
            '<span class="hp">'+str(si+1)+'/'+str(len(slides))+'</span>'
            '</div>'
            '<div class="sc">'+ch+'</div>'
            '</div></div>'
        )
    return out

def build():
    src = "/media/mohamed/projects4/obs_content-mcqs/Week1_Infographic.html"
    with open(src, 'r', encoding='utf-8') as f: full = f.read()
    
    spos = [m.start() for m in re.finditer(r'<div class="sec" id=', full)]
    topics = []
    for i, pos in enumerate(spos):
        end = spos[i+1] if i+1 < len(spos) else len(full)
        sec = full[pos:end]
        m = re.search(r'<div class="sec-hdr" style="background:(#[0-9a-f]+)"[^>]*>.*?<h2>(.*?)</h2>', sec, re.DOTALL)
        color = m.group(1) if m else '#333'
        title = ct(m.group(2)) if m else 'Topic '+str(i+1)
        topics.append((pos, end, title, color))
    
    print(str(len(topics))+" topics")
    SH = []
    sn = [0]
    
    def add(h, title=False):
        sn[0] += 1
        cl = 'sl st' if title else 'sl'
        SH.append('<div class="'+cl+'" data-n="'+str(sn[0])+'">'+h+'</div>')
    
    # Title
    add('<div class="tg" style="background:linear-gradient(135deg,#0f3a5f,#1a237e)"><div class="ti">&#x1F3E5;</div><h1 class="tm">OB/GYN</h1><h2 class="ts">Week 1 &mdash; Physiology &amp; Early Pregnancy</h2><p class="tx">'+str(len(topics))+' Topics</p></div>', True)
    
    # TOC
    toc = ''.join('<div class="tr"><span class="tn" style="background:'+c+'">'+str(i+1)+'</span><span class="tt">'+t+'</span></div>' for i,(_,_,t,c) in enumerate(topics))
    add('<div class="tg" style="background:linear-gradient(135deg,#1a1a2e,#16213e)"><div class="tct">Table of Contents</div><div class="tcl">'+toc+'</div></div>', True)
    
    for ti,(pos,end,tt,tc) in enumerate(topics):
        sec = full[pos:end]
        add('<div class="tg" style="background:linear-gradient(135deg,'+tc+','+tc+'cc)"><div class="tpn">TOPIC '+str(ti+1)+' OF '+str(len(topics))+'</div><h1 class="tpt">'+tt+'</h1></div>', True)
        items = extract_items(sec)
        if not items: continue
        for sh in pack(items, tt, tc, ti+1, len(topics)):
            add(sh)
    
    add('<div class="tg" style="background:linear-gradient(135deg,#1a1a2e,#16213e)"><div class="ti">&#x2705;</div><h1 class="tm">Week 1 Complete</h1><p class="tx">'+str(len(topics))+' Topics &middot; '+str(sn[0])+' Slides</p></div>', True)
    
    total = sn[0]
    numbered = []
    c = 0
    for s in SH:
        c += 1
        numbered.append(s.replace('__N__', str(c)))
    
    print("Slides: "+str(total))
    
    final = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080">
<title>Week 1 &mdash; OB/GYN Slide Deck</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#111;height:100%;overflow:hidden}
body{display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif}
.frame{width:1080px;height:1920px;position:relative;overflow:hidden;background:#fff}
.sl{position:absolute;top:0;left:0;width:1080px;height:1920px;display:none;flex-direction:column}
.sl.active{display:flex}

/* Title slides */
.tg{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#fff;padding:40px;text-align:center}
.ti{font-size:100px;margin-bottom:20px}
.tm{font-size:58px;font-weight:800;margin-bottom:10px;line-height:1.2}
.ts{font-size:30px;font-weight:600;opacity:0.85;line-height:1.4}
.tx{font-size:22px;opacity:0.6;margin-top:8px}
.tpn{font-size:20px;font-weight:700;opacity:0.5;letter-spacing:3px;margin-bottom:10px}
.tpt{font-size:48px;font-weight:800;line-height:1.3}
.tct{font-size:36px;font-weight:800;margin-bottom:24px}
.tcl{width:100%;max-width:860px}
.tr{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.12)}
.tn{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;color:#fff;font-weight:700;font-size:14px;flex-shrink:0}
.tt{font-size:20px;font-weight:500}

/* Content slides */
.sb{display:flex;flex-direction:column;height:100%;background:#fff}
.sb.co .sc{gap:4px}
.hd{display:flex;align-items:center;gap:8px;padding:10px 28px;border-bottom:3px solid #333;background:#f8fafc;flex-shrink:0}
.hn{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;color:#fff;font-weight:700;font-size:13px;flex-shrink:0}
.ht{flex:1;font-size:16px;font-weight:600;color:#334155}
.hp{font-size:13px;color:#94a3b8;font-weight:600}

/* Content area - fills ALL remaining space */
.sc{flex:1;padding:16px 32px 16px 32px;overflow:hidden;display:flex;flex-direction:column;gap:6px}

/* Elements - TIGHT */
.sh{font-size:26px;font-weight:700;color:#1e293b;line-height:1.25;padding-bottom:4px;border-bottom:2px solid #e2e8f0}
.sh2{font-size:22px;font-weight:700;color:#334155;line-height:1.25}
.sh3{font-size:19px;font-weight:600;color:#475569;line-height:1.25}
.pt{font-size:18px;line-height:1.45;color:#334155}
.bl{font-size:18px;line-height:1.4;color:#334155;padding-left:18px;position:relative}
.bl::before{content:"\\2022";position:absolute;left:2px;color:#6366f1;font-weight:900;font-size:20px}

/* Tables - tight */
.tb{width:100%;border-collapse:collapse;font-size:16px}
.tb th{background:#f1f5f9;padding:7px 10px;text-align:left;font-weight:700;border:2px solid #e2e8f0}
.tb td{padding:6px 10px;border:1px solid #e2e8f0}
.tb tr:nth-child(even) td{background:#f8fafc}

/* Callouts - tight */
.cp{padding:8px 14px;border-radius:8px;font-size:17px;line-height:1.4;background:#f0fdf4;border-left:4px solid #22c55e;color:#166534}
.cw{padding:8px 14px;border-radius:8px;font-size:17px;line-height:1.4;background:#fffbeb;border-left:4px solid #f59e0b;color:#92400e}
.cd{padding:8px 14px;border-radius:8px;font-size:17px;line-height:1.4;background:#fef2f2;border-left:4px solid #ef4444;color:#991b1b}
.cn{padding:8px 14px;border-radius:8px;font-size:17px;line-height:1.4;background:#eff6ff;border-left:4px solid #3b82f6;color:#1e40af}
.cs{display:inline-flex;padding:6px 12px;border-radius:6px;background:#f1f5f9;font-size:16px;font-weight:600}

/* Nav */
.nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;padding:8px 20px;background:rgba(0,0,0,0.88);border-radius:12px 12px 0 0;z-index:100}
.nav button{width:38px;height:38px;border:none;border-radius:50%;background:#334155;color:#fff;font-size:16px;cursor:pointer}
.nav button:hover{background:#475569}
.nav .ct2{color:#94a3b8;font-size:13px;font-weight:600;min-width:70px;text-align:center}
.progress{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#6366f1,#8b5cf6);z-index:100;transition:width 0.3s}
</style></head><body>
<div class="progress" id="pg"></div>
<div class="frame">
''' + '\n'.join(numbered) + '''
</div>
<div class="nav">
<button onclick="go(-1)">&#x25C0;</button>
<div class="ct2" id="ct2">1/''' + str(total) + '''</div>
<button onclick="go(1)">&#x25B6;</button>
</div>
<script>
var c=1,t=''' + str(total) + ''';
function show(n){c=Math.max(1,Math.min(t,n));document.querySelectorAll('.sl').forEach(function(s){s.classList.remove('active')});var e=document.querySelector('[data-n="'+c+'"]');if(e)e.classList.add('active');document.getElementById('ct2').textContent=c+'/'+t;document.getElementById('pg').style.width=(c/t*100)+'%'}
function go(d){show(c+d)}
document.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key===' ')go(1);if(e.key==='ArrowLeft')go(-1);if(e.key==='Home')show(1);if(e.key==='End')show(t)});
var sx=0;document.addEventListener('touchstart',function(e){sx=e.touches[0].clientX});
document.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)go(dx<0?1:-1)});
show(1);
</script></body></html>'''
    
    out = "/media/mohamed/projects4/obs_content-mcqs/Week1_Slides.html"
    with open(out, 'w', encoding='utf-8') as f: f.write(final)
    print(str(os.path.getsize(out)//1024)+"KB")

build()
