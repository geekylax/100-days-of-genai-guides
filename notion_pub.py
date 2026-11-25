#!/usr/bin/env python3
"""Publish a Markdown file as a Notion child page. Handles headings, paragraphs,
bullet/numbered lists, images, dividers, quotes, code fences, and inline bold/code/links."""
import os, sys, json, re, time, urllib.request

TOKEN=os.environ.get("NOTION_TOKEN","")
VER="2022-06-28"
API="https://api.notion.com/v1"

def req(method, path, body=None):
    data=json.dumps(body).encode() if body is not None else None
    r=urllib.request.Request(API+path, data=data, method=method,
        headers={"Authorization":f"Bearer {TOKEN}","Notion-Version":VER,"Content-Type":"application/json"})
    try:
        return json.load(urllib.request.urlopen(r, timeout=60))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:400]); raise

# ---------- inline parser ----------
TOKEN_RE=re.compile(r'(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))')
def rich(text):
    out=[]
    for part in TOKEN_RE.split(text):
        if not part: continue
        ann={"bold":False,"italic":False,"strikethrough":False,"underline":False,"code":False,"color":"default"}
        link=None; content=part
        m=re.match(r'\[([^\]]+)\]\(([^)]+)\)$', part)
        if part.startswith('**') and part.endswith('**') and len(part)>4:
            ann["bold"]=True; content=part[2:-2]
        elif part.startswith('`') and part.endswith('`') and len(part)>2:
            ann["code"]=True; content=part[1:-1]
        elif m:
            content=m.group(1); link={"url":m.group(2)}
        # nested bold inside link text
        if link and content.startswith('**') and content.endswith('**'):
            ann["bold"]=True; content=content[2:-2]
        for i in range(0, len(content) or 1, 1900):
            chunk=content[i:i+1900]
            t={"type":"text","text":{"content":chunk}}
            if link: t["text"]["link"]=link
            t["annotations"]=dict(ann)
            out.append(t)
    return out or [{"type":"text","text":{"content":""}}]

def para(text): return {"object":"block","type":"paragraph","paragraph":{"rich_text":rich(text)}}
def heading(n,text):
    k=f"heading_{min(n,3)}"; return {"object":"block","type":k,k:{"rich_text":rich(text)}}
def bullet(text): return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":rich(text)}}
def number(text): return {"object":"block","type":"numbered_list_item","numbered_list_item":{"rich_text":rich(text)}}
def quote(text): return {"object":"block","type":"quote","quote":{"rich_text":rich(text)}}
def divider(): return {"object":"block","type":"divider","divider":{}}
def image(url): return {"object":"block","type":"image","image":{"type":"external","external":{"url":url}}}
def code(text,lang="plain text"): return {"object":"block","type":"code","code":{"rich_text":[{"type":"text","text":{"content":text[:1900]}}],"language":lang}}

def _cells(row):
    row=row.strip()
    if row.startswith("|"): row=row[1:]
    if row.endswith("|"): row=row[:-1]
    return [c.strip() for c in row.split("|")]

def table_block(rows):
    header=_cells(rows[0]); w=len(header)
    def mkrow(r):
        cs=_cells(r)
        cs=(cs+[""]*w)[:w]
        return {"object":"block","type":"table_row","table_row":{"cells":[rich(c) for c in cs]}}
    body=[r for idx,r in enumerate(rows) if idx!=1]  # drop separator row
    return {"object":"block","type":"table","table":{"table_width":w,"has_column_header":True,"has_row_header":False,
            "children":[mkrow(r) for r in body]}}

def _is_table_sep(ln):
    return bool(re.match(r'^\s*\|?[\s:|-]+\|[\s:|-]*$', ln)) and '-' in ln

def md_to_blocks(md):
    lines=md.split("\n"); blocks=[]; title=None; i=0
    while i < len(lines):
        ln=lines[i].rstrip()
        # table: a | row followed by a separator row
        if ln.strip().startswith("|") and i+1<len(lines) and _is_table_sep(lines[i+1]):
            rows=[ln]; j=i+1
            while j<len(lines) and lines[j].strip().startswith("|"):
                rows.append(lines[j].rstrip()); j+=1
            if len(rows)>=2:
                blocks.append(table_block(rows)); i=j; continue
        if ln.startswith("```"):
            lang=ln[3:].strip() or "plain text"; buf=[]; i+=1
            while i<len(lines) and not lines[i].startswith("```"): buf.append(lines[i]); i+=1
            blocks.append(code("\n".join(buf), lang if lang in ("python","javascript","typescript","bash","shell","json","markdown","plain text") else "plain text")); i+=1; continue
        img=re.match(r'!\[([^\]]*)\]\(([^)]+)\)', ln.strip())
        if img: blocks.append(image(img.group(2))); i+=1; continue
        if ln.strip()=="---": blocks.append(divider()); i+=1; continue
        m=re.match(r'(#{1,6})\s+(.*)', ln)
        if m:
            lvl=len(m.group(1)); txt=m.group(2).strip()
            if lvl==1 and title is None: title=txt
            else: blocks.append(heading(lvl, txt))
            i+=1; continue
        if ln.startswith(">"): blocks.append(quote(ln[1:].strip())); i+=1; continue
        m=re.match(r'\s*[-*]\s+(.*)', ln)
        if m: blocks.append(bullet(m.group(1))); i+=1; continue
        m=re.match(r'\s*\d+\.\s+(.*)', ln)
        if m: blocks.append(number(m.group(1))); i+=1; continue
        if ln.strip()=="": i+=1; continue
        blocks.append(para(ln.strip())); i+=1
    return title, blocks

def publish(md_path, parent_page_id, title_override=None, icon=None):
    md=open(md_path).read()
    title, blocks = md_to_blocks(md)
    title=title_override or title or os.path.basename(md_path)
    page={"parent":{"type":"page_id","page_id":parent_page_id},
          "properties":{"title":{"title":[{"type":"text","text":{"content":title}}]}},
          "children":blocks[:100]}
    if icon: page["icon"]={"type":"emoji","emoji":icon}
    res=req("POST","/pages",page)
    pid=res["id"]; url=res["url"]
    # append remaining blocks in batches of 100
    rest=blocks[100:]
    while rest:
        req("PATCH", f"/blocks/{pid}/children", {"children":rest[:100]})
        rest=rest[100:]; time.sleep(0.3)
    return pid, url

if __name__=="__main__":
    # args: md_path parent_id [icon] [title]
    md_path=sys.argv[1]; parent=sys.argv[2]
    icon=sys.argv[3] if len(sys.argv)>3 else None
    title=sys.argv[4] if len(sys.argv)>4 else None
    pid,url=publish(md_path, parent, title, icon)
    print("PAGE_URL", url)
    print("PAGE_ID", pid)
