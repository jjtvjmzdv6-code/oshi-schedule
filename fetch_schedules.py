import json, re, hashlib
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

SOURCES = [
 ("skz","https://straykids.jype.com/schedule","Stray Kids"),
 ("skz","https://straykids.jype.com/notice","Stray Kids"),
 ("ateez","https://ateez-official.jp/contents/schedule","ATEEZ"),
 ("bnd","https://boynextdoor-official.jp/Schedule","BOYNEXTDOOR"),
 ("ive","https://ive-official.jp/mob/news/diarKiji.php?cd=SCHEDULE&ima=0146&site=DIVE","IVE"),
]
MONTHS = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
DATE_PATTERNS = [
 re.compile(r"(20\d{2})[./年-](\d{1,2})[./月-](\d{1,2})日?"),
 re.compile(r"(20\d{2})\.(\d{1,2})\.(\d{1,2})"),
]
def date_from(text):
 for p in DATE_PATTERNS:
  m=p.search(text)
  if m:
   try: return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
   except ValueError: pass
 return None
def main():
 headers={"User-Agent":"Mozilla/5.0 (compatible; IdolScheduleBot/1.0; +https://github.com)"}
 events=[]; seen=set()
 for group,url,label in SOURCES:
  try:
   r=requests.get(url,headers=headers,timeout=25);r.raise_for_status()
   soup=BeautifulSoup(r.text,"html.parser")
   # Use visible text blocks; schedule pages often separate date and title into adjacent elements.
   for node in soup.select("li, article, tr, .schedule, .item, .list-item, a"):
    txt=" ".join(node.get_text(" ",strip=True).split())
    if len(txt)<12 or len(txt)>700: continue
    dt=date_from(txt)
    if not dt:
     parent=node.parent
     if parent:
      combined=" ".join(parent.get_text(" ",strip=True).split())
      dt=date_from(combined)
      if dt and len(combined)<900: txt=combined
    if not dt: continue
    # avoid importing old schedules
    if dt < datetime.now().strftime("%Y-%m-%d"): continue
    title=re.sub(r"20\d{2}[./年-]\d{1,2}[./月-]\d{1,2}日?","",txt).strip(" |·-")
    title=re.sub(r"\s+"," ",title)
    if len(title)<4: continue
    a=node if node.name=="a" else node.find("a",href=True)
    link=urljoin(url,a.get("href")) if a else url
    cat="公式スケジュール"
    for word,kind in [("TV","TV"),("RADIO","RADIO"),("LIVE","LIVE/EVENT"),("EVENT","LIVE/EVENT"),("RELEASE","RELEASE"),("MAGAZINE","MAGAZINE"),("WEB","WEB")]:
     if word.lower() in txt.lower(): cat=kind; break
    key=(group,dt,title)
    if key in seen: continue
    seen.add(key)
    events.append({"group":group,"date":dt,"title":title[:220],"category":cat,"url":link})
  except Exception as e:
   print(f"Could not read {url}: {e}")
 events.sort(key=lambda x:(x["date"],x["group"],x["title"]))
 data={"updated_at":datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"),"events":events,"sources":[{"group":g,"url":u} for g,u,_ in SOURCES]}
 with open("schedules.json","w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)
 print(f"Saved {len(events)} upcoming entries")
if __name__=="__main__": main()
