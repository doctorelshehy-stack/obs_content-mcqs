#!/usr/bin/env python3
"""
Parse Week1_Infographic.html and generate Week1_Slides.html
as a VERTICAL (1080x1920) fixed-size slide deck with ALL content.
"""

import re
import html
import os

INPUT_FILE = 'Week1_Infographic.html'
OUTPUT_FILE = 'Week1_Slides.html'

TOPIC_COLORS = [
    ('#0f3a5f', '#1a5276'),
    ('#1b5e20', '#2e7d32'),
    ('#c62828', '#d32f2f'),
    ('#1565c0', '#1976d2'),
    ('#e65100', '#f57c00'),
    ('#b71c1c', '#c62828'),
    ('#6a1b9a', '#7b1fa2'),
    ('#4527a0', '#512da8'),
    ('#d32f2f', '#e53935'),
    ('#f57f17', '#ff8f00'),
    ('#00695c', '#00897b'),
    ('#283593', '#3949ab'),
    ('#880e4f', '#ad1457'),
]

TOPIC_ICONS = ['🔬', '🤰', '🔍', '🏥', '⚠️', '📍', '🧬', '💊', '🩸', '💉', '🦠', '🫁', '🅰️']


def strip_tags(text):
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def split_into_topics(raw_html):
    header_pattern = r'<div class="sec" id="([^"]+)">\s*<div class="sec-hdr"[^>]*><h2>([^<]+)</h2>'
    headers = list(re.finditer(header_pattern, raw_html))
    topics = []
    for i, match in enumerate(headers):
        start = match.start()
        end = headers[i + 1].start() if i + 1 < len(headers) else raw_html.rfind('<div class="footer">')
        section_html = raw_html[start:end]
        topics.append({
            'id': match.group(1),
            'title': match.group(2).strip(),
            'html': section_html,
            'index': i
        })
    return topics


def clean_inner_html(content):
    """Remove nested DOCTYPE, html, head, body structures."""
    content = re.sub(r'<!DOCTYPE[^>]*>', '', content)
    content = re.sub(r'<html[^>]*>', '', content)
    content = re.sub(r'</html>', '', content)
    content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL)
    content = re.sub(r'<body>', '', content)
    content = re.sub(r'</body>', '', content)
    content = re.sub(r'<meta[^>]*>', '', content)
    content = re.sub(r'<title>[^<]*</title>', '', content)
    content = re.sub(r'<link[^>]*>', '', content)
    return content


def extract_all_blocks(section_html):
    """Extract ALL content blocks from a section using multiple strategies."""
    blocks = []
    seen_texts = set()
    
    # Get the sec-bd content
    sec_bd_match = re.search(r'<div class="sec-bd"[^>]*>(.*)', section_html, re.DOTALL)
    if not sec_bd_match:
        return blocks
    
    content = clean_inner_html(sec_bd_match.group(1))
    
    def add_block(btype, bdata, btext, extra_key=''):
        """Add a block if not already seen."""
        if btype in ('ul', 'ol'):
            key = extra_key or str(btext[:5]) if isinstance(btext, list) and btext else str(btext)[:50]
        elif btype == 'table':
            key = str(btext[0][:3]) if btext and btext[0] else 'table'
        else:
            key = (extra_key or str(btext))[:80]
        
        if key not in seen_texts:
            seen_texts.add(key)
            blocks.append((btype, bdata, btext))
    
    # === STRATEGY 1: Extract by structural position ===
    # Process the content sequentially to maintain order
    
    # Find all significant elements with their positions
    elements = []
    
    # Find all headings
    for m in re.finditer(r'<h(\d)[^>]*>(.*?)</h\1>', content, re.DOTALL):
        level = int(m.group(1))
        text = strip_tags(m.group(2)).strip()
        if text and len(text) > 1:
            elements.append((m.start(), 'heading', level, text))
    
    # Find all paragraphs
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        if text and len(text) > 2:
            elements.append((m.start(), 'paragraph', 0, text))
    
    # Find all unordered lists (non-overlapping with nested)
    for m in re.finditer(r'<ul[^>]*>(.*?)</ul>', content, re.DOTALL):
        items = []
        for li in re.finditer(r'<li[^>]*>(.*?)</li>', m.group(1), re.DOTALL):
            item_text = strip_tags(li.group(1)).strip()
            if item_text and len(item_text) > 1:
                items.append(item_text)
        if items:
            elements.append((m.start(), 'ul', 0, items))
    
    # Find all ordered lists
    for m in re.finditer(r'<ol[^>]*>(.*?)</ol>', content, re.DOTALL):
        items = []
        for li in re.finditer(r'<li[^>]*>(.*?)</li>', m.group(1), re.DOTALL):
            item_text = strip_tags(li.group(1)).strip()
            if item_text and len(item_text) > 1:
                items.append(item_text)
        if items:
            elements.append((m.start(), 'ol', 0, items))
    
    # Find all tables
    for m in re.finditer(r'<table[^>]*>(.*?)</table>', content, re.DOTALL):
        rows = []
        for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.DOTALL):
            cells = []
            for td in re.finditer(r'<t[hd][^>]*>(.*?)</t[hd]>', tr.group(1), re.DOTALL):
                cells.append(strip_tags(td.group(1)).strip())
            if cells:
                rows.append(cells)
        if rows:
            elements.append((m.start(), 'table', 0, rows))
    
    # Find all callout boxes (broad match)
    for m in re.finditer(r'<div class="callout\s+(\S+)"[^>]*>', content):
        cls = m.group(1)
        start = m.end()
        # Find end: next callout, next section-level element, or end of content
        next_callout = re.search(r'<div class="callout\s+', content[start:])
        next_section = re.search(r'</section>|<div class="sec\b|<section\b', content[start:])
        
        if next_callout and (not next_section or next_callout.start() < next_section.start()):
            end = start + next_callout.start()
        elif next_section:
            end = start + next_section.start()
        else:
            end = min(start + 5000, len(content))
        
        block_text = content[start:end]
        # Remove nested divs
        block_text_clean = re.sub(r'<div[^>]*>.*?</div>', '', block_text, flags=re.DOTALL)
        text = strip_tags(block_text_clean).strip()
        text = re.sub(r'\s+', ' ', text)
        
        if text and len(text) > 5:
            ctype = 'pearl' if 'pearl' in cls else 'warn' if 'warn' in cls else 'danger' if 'danger' in cls else 'note'
            elements.append((m.start(), 'callout', ctype, text))
    
    # Find defbox
    for m in re.finditer(r'<div class="defbox">(.*?)</div>\s*</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'definition', 0, text))
    
    # Find keydef
    for m in re.finditer(r'<div class="keydef">(.*?)</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'definition', 0, text))
    
    # Find note divs (standalone, not inside callout)
    for m in re.finditer(r'<div class="note">(.*?)</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'callout', 'note', text))
    
    # Find pearl divs (standalone)
    for m in re.finditer(r'<div class="pearl">(.*?)</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'callout', 'pearl', text))
    
    # Find warn divs (standalone)
    for m in re.finditer(r'<div class="warn">(.*?)</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'callout', 'warn', text))
    
    # Find stat/mini-card content
    for m in re.finditer(r'<div class="mini-card">(.*?)</div>\s*</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 3:
            elements.append((m.start(), 'stat', 0, text))
    
    # Find card content (label/val pairs)
    for m in re.finditer(r'<div class="card">(.*?)</div>\s*</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'stat', 0, text))
    
    # Find stage/eden/type cards
    for pattern in ['stage', 'eden-card', 'type-card', 'classif-card', 'class-card',
                     'flow-card', 'clinical-card', 'pe-card', 'pe-tx-card',
                     'risk-card', 'invest-card', 'tx-card', 'rx-card', 'mgmt-card',
                     'eti-card', 'crit-card', 'stat']:
        for m in re.finditer(rf'<div class="{pattern}[^"]*">(.*?)</div>\s*</div>', content, re.DOTALL):
            text = strip_tags(m.group(1)).strip()
            text = re.sub(r'\s+', ' ', text)
            if text and len(text) > 5:
                elements.append((m.start(), 'paragraph', 0, text))
    
    # Find comparison-row content
    for m in re.finditer(r'<div class="comparison-row">(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 5:
            elements.append((m.start(), 'paragraph', 0, text))
    
    # Sort by position to maintain document order
    elements.sort(key=lambda x: x[0])
    
    # Convert to blocks
    for elem in elements:
        if elem[1] == 'heading':
            add_block('heading', elem[2], elem[3])
        elif elem[1] == 'paragraph':
            add_block('paragraph', 0, elem[3])
        elif elem[1] == 'ul':
            add_block('ul', 0, elem[3])
        elif elem[1] == 'ol':
            add_block('ol', 0, elem[3])
        elif elem[1] == 'table':
            add_block('table', 0, elem[3])
        elif elem[1] == 'callout':
            add_block('callout', elem[2], elem[3])
        elif elem[1] == 'definition':
            add_block('definition', 0, elem[3])
        elif elem[1] == 'stat':
            add_block('stat', 0, elem[3])
    
    return blocks


def blocks_to_html(blocks):
    """Convert text blocks to slide HTML content."""
    html_parts = []
    
    for btype, bdata, btext in blocks:
        if btype == 'heading':
            level = bdata
            if level == 3:
                html_parts.append(f'<h3 class="slide-h3">{html.escape(btext)}</h3>')
            elif level == 4:
                html_parts.append(f'<h4 class="slide-h4">{html.escape(btext)}</h4>')
            elif level == 5:
                html_parts.append(f'<h5 class="slide-h5">{html.escape(btext)}</h5>')
            else:
                html_parts.append(f'<h4 class="slide-h4">{html.escape(btext)}</h4>')
        elif btype == 'paragraph':
            html_parts.append(f'<p class="slide-p">{html.escape(btext)}</p>')
        elif btype == 'ul':
            html_parts.append('<ul class="slide-ul">')
            for item in btext:
                html_parts.append(f'  <li>{html.escape(item)}</li>')
            html_parts.append('</ul>')
        elif btype == 'ol':
            html_parts.append('<ol class="slide-ol">')
            for item in btext:
                html_parts.append(f'  <li>{html.escape(item)}</li>')
            html_parts.append('</ol>')
        elif btype == 'table':
            rows = btext
            if rows:
                html_parts.append('<div class="slide-table-wrap"><table class="slide-table">')
                for i, row in enumerate(rows):
                    html_parts.append('<tr>')
                    tag = 'th' if i == 0 else 'td'
                    for cell in row:
                        html_parts.append(f'  <{tag}>{html.escape(cell)}</{tag}>')
                    html_parts.append('</tr>')
                html_parts.append('</table></div>')
        elif btype == 'callout':
            ctype = bdata
            icon = '💎' if ctype == 'pearl' else '⚠️' if ctype == 'warn' else '🚨' if ctype == 'danger' else '📝'
            label = 'Clinical Pearl' if ctype == 'pearl' else 'Warning' if ctype == 'warn' else 'Danger' if ctype == 'danger' else 'Note'
            html_parts.append(f'<div class="callout-box {ctype}"><div class="callout-label">{icon} {label}</div><div class="callout-text">{html.escape(btext)}</div></div>')
        elif btype == 'definition':
            html_parts.append(f'<div class="def-box">{html.escape(btext)}</div>')
        elif btype == 'stat':
            html_parts.append(f'<div class="stat-box">{html.escape(btext)}</div>')
    
    return '\n'.join(html_parts)


def estimate_block_size(btype, bdata, btext):
    """Estimate how much vertical space a block takes."""
    if btype == 'heading':
        return 2
    elif btype == 'paragraph':
        return max(2, len(btext) // 80 + 2)
    elif btype in ('ul', 'ol'):
        return len(btext) + 1
    elif btype == 'table':
        return len(btext) + 2
    elif btype == 'callout':
        return max(3, len(btext) // 60 + 3)
    elif btype == 'definition':
        return 3
    elif btype == 'stat':
        return 2
    return 2


def make_content_slide(topic_title, topic_idx, icon, color1, color2, blocks_html):
    """Generate a single content slide."""
    return f'''
    <div class="slide content-slide">
      <div class="slide-header" style="background: linear-gradient(135deg, {color1}, {color2})">
        <h2>{icon} {html.escape(topic_title)} <span class="slide-topic-num">({topic_idx+1}/13)</span></h2>
      </div>
      <div class="slide-body">
        {blocks_html}
      </div>
    </div>'''


def generate_slide_html():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_html = f.read()
    
    topics = split_into_topics(raw_html)
    all_slides = []
    
    # Title slide
    all_slides.append('''
    <div class="slide title-slide">
      <div class="title-content">
        <div class="title-icon">📚</div>
        <h1 class="main-title">Week 1</h1>
        <h2 class="sub-title">Physiology & Early Pregnancy</h2>
        <p class="title-desc">Comprehensive Study Guide — All 13 Topics</p>
        <div class="title-stats">
          <div class="tstat"><div class="tstat-n">13</div><div class="tstat-l">Topics</div></div>
          <div class="tstat"><div class="tstat-n">930+</div><div class="tstat-l">Key Points</div></div>
          <div class="tstat"><div class="tstat-n">138</div><div class="tstat-l">Clinical Pearls</div></div>
        </div>
      </div>
    </div>''')
    
    # TOC slide
    toc_items = ''
    for i, topic in enumerate(topics):
        color = TOPIC_COLORS[i % len(TOPIC_COLORS)][0]
        icon = TOPIC_ICONS[i % len(TOPIC_ICONS)]
        toc_items += f'<div class="toc-item" style="border-left: 4px solid {color}"><span class="toc-icon">{icon}</span> <span class="toc-num">{i+1}.</span> {html.escape(topic["title"])}</div>\n'
    
    all_slides.append(f'''
    <div class="slide toc-slide">
      <div class="slide-header" style="background: linear-gradient(135deg, #1a1a2e, #16213e)">
        <h2>📋 Table of Contents</h2>
      </div>
      <div class="slide-body toc-body">
        {toc_items}
      </div>
    </div>''')
    
    # Process each topic
    for i, topic in enumerate(topics):
        color1, color2 = TOPIC_COLORS[i % len(TOPIC_COLORS)]
        icon = TOPIC_ICONS[i % len(TOPIC_ICONS)]
        
        # Topic title slide
        all_slides.append(f'''
    <div class="slide topic-title-slide">
      <div class="topic-title-bg" style="background: linear-gradient(135deg, {color1}, {color2})">
        <div class="topic-num">{icon} Topic {i+1}</div>
        <h2 class="topic-main-title">{html.escape(topic["title"])}</h2>
      </div>
    </div>''')
        
        blocks = extract_all_blocks(topic['html'])
        
        if not blocks:
            continue
        
        # Split into slides
        current_slide_blocks = []
        current_size = 0
        MAX_SIZE = 14  # ~14 "lines" per slide
        
        for btype, bdata, btext in blocks:
            size = estimate_block_size(btype, bdata, btext)
            
            # Large table - split it
            if btype == 'table' and len(btext) > 6:
                # Emit current slide first
                if current_slide_blocks:
                    slide_html = blocks_to_html(current_slide_blocks)
                    all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                    current_slide_blocks = []
                    current_size = 0
                
                # Split table
                for j in range(0, len(btext), 6):
                    chunk = btext[j:j+6]
                    slide_html = blocks_to_html([('table', 0, chunk)])
                    all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                continue
            
            # Large list - split it
            if btype in ('ul', 'ol') and len(btext) > 10:
                if current_slide_blocks:
                    slide_html = blocks_to_html(current_slide_blocks)
                    all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                    current_slide_blocks = []
                    current_size = 0
                
                for j in range(0, len(btext), 10):
                    chunk = btext[j:j+10]
                    slide_html = blocks_to_html([(btype, 0, chunk)])
                    all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                continue
            
            # Large callout - split if needed
            if btype == 'callout' and size > 8:
                if current_slide_blocks:
                    slide_html = blocks_to_html(current_slide_blocks)
                    all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                    current_slide_blocks = []
                    current_size = 0
                
                # Split callout text into paragraphs
                words = btext.split()
                chunk_size = 80  # words per chunk
                for j in range(0, len(words), chunk_size):
                    chunk = ' '.join(words[j:j+chunk_size])
                    slide_html = blocks_to_html([(btype, bdata, chunk)])
                    all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                continue
            
            # Check if adding this block exceeds capacity
            if current_size + size > MAX_SIZE and current_slide_blocks:
                slide_html = blocks_to_html(current_slide_blocks)
                all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
                current_slide_blocks = []
                current_size = 0
            
            current_slide_blocks.append((btype, bdata, btext))
            current_size += size
        
        # Emit remaining
        if current_slide_blocks:
            slide_html = blocks_to_html(current_slide_blocks)
            all_slides.append(make_content_slide(topic['title'], i, icon, color1, color2, slide_html))
    
    # End slide
    all_slides.append('''
    <div class="slide end-slide">
      <div class="title-content">
        <div class="title-icon">✅</div>
        <h1 class="main-title">End of Week 1</h1>
        <h2 class="sub-title">Physiology & Early Pregnancy</h2>
        <p class="title-desc">13 Topics · 930+ Key Points · 138 Clinical Pearls</p>
        <p class="title-desc" style="margin-top:20px;font-size:18px;color:rgba(255,255,255,0.6)">Swipe or use arrow keys to navigate</p>
      </div>
    </div>''')
    
    total_slides = len(all_slides)
    
    # Build complete HTML
    html_output = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, initial-scale=1.0">
<title>Week 1 — Physiology & Early Pregnancy — Slide Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; overflow-x: hidden; font-family: 'Inter', -apple-system, sans-serif; background: #111; color: #1f2a37; }}
.slide-container {{ width: 1080px; margin: 0 auto; }}
.slide {{ width: 1080px; height: 1920px; position: relative; overflow: hidden; page-break-after: always; background: #ffffff; }}

.title-slide {{ background: linear-gradient(135deg, #0f3a5f 0%, #1a1a2e 50%, #16213e 100%); display: flex; align-items: center; justify-content: center; }}
.title-content {{ text-align: center; padding: 60px; }}
.title-icon {{ font-size: 80px; margin-bottom: 30px; }}
.main-title {{ font-size: 72px; font-weight: 800; color: #fff; margin-bottom: 10px; letter-spacing: -2px; }}
.sub-title {{ font-size: 42px; font-weight: 600; color: rgba(255,255,255,0.85); margin-bottom: 30px; }}
.title-desc {{ font-size: 22px; color: rgba(255,255,255,0.6); margin-bottom: 40px; }}
.title-stats {{ display: flex; justify-content: center; gap: 40px; margin-top: 40px; }}
.tstat {{ background: rgba(255,255,255,0.1); border-radius: 16px; padding: 24px 40px; text-align: center; }}
.tstat-n {{ font-size: 42px; font-weight: 800; color: #fff; }}
.tstat-l {{ font-size: 16px; color: rgba(255,255,255,0.6); text-transform: uppercase; letter-spacing: 1px; }}

.toc-slide {{ display: flex; flex-direction: column; }}
.toc-body {{ padding: 30px 50px; flex: 1; overflow-y: auto; }}
.toc-item {{ padding: 14px 20px; margin: 6px 0; background: #f8f9fa; border-radius: 10px; font-size: 22px; font-weight: 500; display: flex; align-items: center; gap: 12px; }}
.toc-icon {{ font-size: 24px; }}
.toc-num {{ font-weight: 700; color: #0f3a5f; min-width: 30px; }}

.topic-title-slide {{ display: flex; align-items: center; justify-content: center; }}
.topic-title-bg {{ width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 60px; }}
.topic-num {{ font-size: 28px; color: rgba(255,255,255,0.7); margin-bottom: 30px; text-transform: uppercase; letter-spacing: 3px; font-weight: 600; }}
.topic-main-title {{ font-size: 56px; font-weight: 800; color: #fff; line-height: 1.2; max-width: 900px; }}

.content-slide {{ display: flex; flex-direction: column; }}
.slide-header {{ padding: 20px 40px; color: #fff; flex-shrink: 0; }}
.slide-header h2 {{ font-size: 26px; font-weight: 700; line-height: 1.3; }}
.slide-topic-num {{ font-weight: 400; opacity: 0.7; font-size: 20px; }}
.slide-body {{ flex: 1; padding: 24px 40px 30px; overflow-y: auto; background: #fff; }}

.slide-h3 {{ font-size: 28px; font-weight: 700; color: #0f3a5f; margin: 18px 0 10px; padding-bottom: 6px; border-bottom: 2px solid #e3e8ef; }}
.slide-h4 {{ font-size: 24px; font-weight: 600; color: #1e6091; margin: 14px 0 8px; }}
.slide-h5 {{ font-size: 21px; font-weight: 600; color: #2a8fb5; margin: 10px 0 6px; }}
.slide-p {{ font-size: 20px; line-height: 1.55; margin: 6px 0; color: #374151; }}
.slide-ul, .slide-ol {{ margin: 6px 0 10px; padding-left: 28px; }}
.slide-ul li, .slide-ol li {{ font-size: 19px; line-height: 1.5; margin: 4px 0; color: #374151; }}
.slide-ul li::marker {{ color: #0f3a5f; font-weight: bold; }}

.slide-table-wrap {{ overflow-x: auto; margin: 10px 0; }}
.slide-table {{ width: 100%; border-collapse: collapse; font-size: 17px; }}
.slide-table th, .slide-table td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; vertical-align: top; }}
.slide-table th {{ background: #0f3a5f; color: #fff; font-weight: 600; font-size: 16px; white-space: nowrap; }}
.slide-table tr:nth-child(even) td {{ background: #f8f9fa; }}

.callout-box {{ border-left: 4px solid; padding: 12px 16px; margin: 10px 0; border-radius: 8px; font-size: 18px; line-height: 1.5; }}
.callout-box.pearl {{ border-color: #2e7d32; background: #eaf6ec; }}
.callout-box.warn {{ border-color: #e65100; background: #fff3e0; }}
.callout-box.danger {{ border-color: #c62828; background: #fdecea; }}
.callout-box.note {{ border-color: #1565c0; background: #e3f2fd; }}
.callout-label {{ font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
.callout-box.pearl .callout-label {{ color: #1b5e20; }}
.callout-box.warn .callout-label {{ color: #e65100; }}
.callout-box.danger .callout-label {{ color: #c62828; }}
.callout-box.note .callout-label {{ color: #1565c0; }}
.callout-text {{ color: #374151; }}

.def-box {{ background: #f0f4f8; border: 2px solid #0f3a5f; border-radius: 10px; padding: 14px 18px; margin: 10px 0; font-size: 19px; font-weight: 500; color: #0f3a5f; }}
.stat-box {{ background: linear-gradient(135deg, #f0f4f8, #e8f0f6); border-radius: 10px; padding: 12px 18px; margin: 6px 0; font-size: 18px; font-weight: 500; text-align: center; color: #0f3a5f; }}

.end-slide {{ background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #1b5e20 100%); display: flex; align-items: center; justify-content: center; }}

.nav-bar {{ position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 1080px; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px); display: flex; align-items: center; justify-content: space-between; padding: 10px 30px; z-index: 10000; border-top: 1px solid rgba(255,255,255,0.1); }}
.nav-btn {{ background: rgba(255,255,255,0.15); border: none; color: #fff; font-size: 24px; padding: 8px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: background 0.2s; }}
.nav-btn:hover {{ background: rgba(255,255,255,0.3); }}
.nav-btn:disabled {{ opacity: 0.3; cursor: default; }}
.nav-counter {{ color: rgba(255,255,255,0.8); font-size: 18px; font-weight: 500; }}
.nav-progress {{ flex: 1; height: 3px; background: rgba(255,255,255,0.2); margin: 0 20px; border-radius: 2px; }}
.nav-progress-fill {{ height: 100%; background: #4ade80; border-radius: 2px; transition: width 0.3s; }}

@media print {{ .nav-bar {{ display: none; }} .slide {{ page-break-after: always; }} }}
</style>
</head>
<body>
<div class="slide-container" id="slideContainer">
'''
    
    for slide in all_slides:
        html_output += slide + '\n'
    
    html_output += f'''
</div>
<div class="nav-bar">
  <button class="nav-btn" id="prevBtn" onclick="prevSlide()">◀ Prev</button>
  <div class="nav-progress"><div class="nav-progress-fill" id="progressFill"></div></div>
  <span class="nav-counter" id="slideCounter">1 / {total_slides}</span>
  <div class="nav-progress"><div class="nav-progress-fill" id="progressFill2"></div></div>
  <button class="nav-btn" id="nextBtn" onclick="nextSlide()">Next ▶</button>
</div>
<script>
const totalSlides = {total_slides};
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
function showSlide(n) {{
  if (n < 0 || n >= totalSlides) return;
  slides[currentSlide].style.display = 'none';
  currentSlide = n;
  slides[currentSlide].style.display = 'block';
  document.getElementById('slideCounter').textContent = (currentSlide + 1) + ' / ' + totalSlides;
  document.getElementById('prevBtn').disabled = currentSlide === 0;
  document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
  const pct = ((currentSlide + 1) / totalSlides * 100).toFixed(1);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressFill2').style.width = pct + '%';
  window.scrollTo(0, 0);
}}
function nextSlide() {{ showSlide(currentSlide + 1); }}
function prevSlide() {{ showSlide(currentSlide - 1); }}
document.addEventListener('keydown', function(e) {{
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {{ e.preventDefault(); nextSlide(); }}
  else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {{ e.preventDefault(); prevSlide(); }}
  else if (e.key === 'Home') {{ e.preventDefault(); showSlide(0); }}
  else if (e.key === 'End') {{ e.preventDefault(); showSlide(totalSlides - 1); }}
}});
let touchStartX = 0, touchStartY = 0;
document.addEventListener('touchstart', function(e) {{ touchStartX = e.touches[0].clientX; touchStartY = e.touches[0].clientY; }}, {{ passive: true }});
document.addEventListener('touchend', function(e) {{
  const dx = e.changedTouches[0].clientX - touchStartX;
  const dy = e.changedTouches[0].clientY - touchStartY;
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {{ if (dx < 0) nextSlide(); else prevSlide(); }}
}}, {{ passive: true }});
slides.forEach((s, i) => {{ s.style.display = i === 0 ? 'block' : 'none'; }});
showSlide(0);
</script>
</body>
</html>'''
    
    return html_output


if __name__ == '__main__':
    print("Generating slide deck...")
    output = generate_slide_html()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)
    
    size = os.path.getsize(OUTPUT_FILE)
    slide_count = output.count('class="slide ')
    
    print(f"Generated {OUTPUT_FILE}")
    print(f"File size: {size:,} bytes ({size/1024:.1f} KB)")
    print(f"Total slides: {slide_count}")
