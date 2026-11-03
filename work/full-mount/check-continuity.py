import sys,json,inspect
from pathlib import Path
sys.path.insert(0,'work/full-mount')
import director
import mount_reviewed_film as film
records=[]
for name in ('seat','walker','stand','climber','big_mountain','pm_full','pm_crawl','bulb','paper_stack'):
 original=getattr(film,name);signature=inspect.signature(original)
 def wrapper(*args,_original=original,_signature=signature,_name=name,**kwargs):
  bound=_signature.bind(*args,**kwargs);bound.apply_defaults()
  values={k:v for k,v in bound.arguments.items() if k in ('beard','grey','b','bulb_b','stack','pack','paper_count','n','beard_trail','beard_tail','pm_beard','pm_grey','pm_papers','dot_b','st','beard_wind')}
  records.append(dict(draw=_name,**values))
  return _original(*args,**kwargs)
 setattr(film,name,wrapper)
manifest=json.loads(Path('work/full-mount/continuity-edit/edit-decisions.json').read_text())
shots={s['name']:s for s in film.SHOTS};audit=[]
for entry in manifest:
 samples=[]
 for n in [entry['source_frames'][0],entry['source_frames'][1]-1]:
  records.clear();film.NOW=n/12;shots[entry['shot']]['draw'](n/12,n)
  samples.append(dict(frame=n,draw_parameters=list(records)))
 audit.append(dict(shot=entry['shot'],samples=samples))
Path('work/full-mount/reviewed-edit/continuity-audit.json').write_text(json.dumps(audit,indent=2))
print('Audited first and last retained frame of',len(audit),'shots')
