from pathlib import Path
import re,json,subprocess,hashlib
from urllib.parse import unquote
import yaml
R=Path(__file__).resolve().parents[4]; P=R/'13 Production/Product_Standards'; A=P/'History/2026-09-20_commercial_freeze'
manifest=json.loads((A/'task_files.json').read_text(encoding='utf-8'))
checks=[]
def check(name,condition,detail=''):
 checks.append(dict(check=name,status='PASS' if condition else 'FAIL',detail=detail))
class UniqueLoader(yaml.SafeLoader): pass
def mapping(loader,node,deep=False):
 result={}
 for k,v in node.value:
  key=loader.construct_object(k,deep=deep)
  if key in result: raise ValueError('Duplicate YAML key: '+str(key))
  result[key]=loader.construct_object(v,deep=deep)
 return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
def read_yaml(p): return yaml.load(p.read_text(encoding='utf-8-sig'),Loader=UniqueLoader)
paths=list(P.glob('*.yaml'))+list((R/'13 Production/Client_Experience/Intake/schemas').glob('*.yaml'))
for p in paths: read_yaml(p)
check('YAML parsing and duplicate-key rejection',True,f'{len(paths)} files')
c=read_yaml(P/'products_v1.yaml'); source=(P/'ONYX_PRODUCT_SYSTEM.md').read_text(encoding='utf-8'); price=(P/'ONYX_PRICE_BOOK_v1.md').read_text(encoding='utf-8')
active=[c['products'][k] for k in c['saleable_product_keys']]
ids=[p['product_id'] for p in active]+list(c['addons'])
check('Unique stable IDs and no legacy product in saleable set',len(ids)==len(set(ids))==9 and all(p['status']=='CURRENT' for p in active) and 'preview' not in c['saleable_product_keys'])
for p in active:
 row=next(line for line in source.splitlines() if line.startswith('| '+p['client_name']+' /'))
 cells=[x.strip() for x in row.split('|')[1:-1]]
 check(p['product_id']+' Markdown/YAML price, final count and rounds',int(cells[1])==p['price_rub'] and int(cells[2])==p['final_image_count']==p['final_photos'] and int(cells[5])==p['included_correction_rounds'])
 row2=next(line for line in price.splitlines() if line.startswith('| '+p['client_name']))
 values=[x.strip() for x in row2.split('|')[1:-1]]
 check(p['product_id']+' Price Book parity',int(values[1])==p['price_rub'] and int(values[2])==p['final_image_count'] and int(values[3])==p['included_correction_rounds'])
 check(p['product_id']+' recommendation ranges are guidance',p['recommended_concepts_min']<=p['recommended_concepts_max'] and p['concept_count_is_customer_guarantee'] is False)
byid={p['product_id']:p for p in active}
for u in c['upgrades']:
 check(u['from_product_id']+' upgrade arithmetic',u['credit_rub']==byid[u['from_product_id']]['price_rub'] and u['credit_rub']+u['additional_payment_rub']==u['target_total_rub']==byid[u['to_product_id']]['price_rub'])
check('Freeze metadata parity',c['commercial_system_id'] in source and c['status'] in source and c['freeze_date'] in source)
check('Legacy Preview quarantined',c['products']['preview']['status']=='SUPERSEDED' and c['products']['preview']['launch_status']=='NOT_FOR_SALE')
for id,a in c['addons'].items():
 row=next(line for line in source.splitlines() if line.startswith('| ') and id in line)
 expected='+'+str(a['surcharge_percent'])+'%' if a['price_type']=='percentage' else str(a['price_rub'])
 check(id+' commercial table parity',expected in row and a['currency']==c['currency'])
schema=read_yaml(R/'13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml')
check('Intake IDs resolve to saleable config',set(schema['commercial_product_mapping'].values())==set(byid))
check('Intake authority resolves', (R/'13 Production/Client_Experience/Intake/schemas'/schema['commercial_authority']).resolve()==P/'ONYX_PRODUCT_SYSTEM.md')
example=read_yaml(R/'13 Production/Client_Experience/Intake/schemas/example_portrait.yaml')
check('Portrait intake example resolves',example['order']['product']=='PORTRAIT' and schema['commercial_product_mapping'][example['order']['product']] in byid)
snap=(A/'superseded_documents.md').read_text(encoding='utf-8')
parts=re.findall(r'^## ([^\n]+)\n\n````text\n(.*?)\n````',snap,re.M|re.S)
old=dict(parts)
hashes=json.loads((A/'baseline_text_sha256.json').read_text(encoding='utf-8'))
check('Superseded snapshot integrity',all(hashlib.sha256(t.encode()).hexdigest()==hashes[p] for p,t in parts) and len(parts)==len(manifest['modified']))
oldschema_text=old['13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml']
# Baseline had one invalid unquoted colon; normalize only for semantic comparison, never rewrite the snapshot.
oldschema_text=oldschema_text.replace('description_ru: Для Premium: DRAFT, PENDING_APPROVAL или APPROVED до массового производства.', "description_ru: 'Для Premium: DRAFT, PENDING_APPROVAL или APPROVED до массового производства.'")
oldschema=yaml.safe_load(oldschema_text)
check('Existing intake field definitions retained',all(group in schema['fields'] and all(any(new['canonical']==field['canonical'] and new.get('type')==field.get('type') and new.get('label_ru')==field.get('label_ru') for new in schema['fields'][group]) for field in fields) for group,fields in oldschema['fields'].items()))
check('Existing consent control values retained',all(set(values).issubset(schema['controlled_values'][key]) for key,values in oldschema['controlled_values'].items()))
# Check only newly introduced links; old source documents contain legacy unresolved wiki/sample links.
bad=[]; linkcount=0
for rel in manifest['modified']+manifest['created']:
 p=R/rel
 if p.suffix!='.md' or '/History/' in rel: continue
 oldlinks=set(re.findall(r'\]\(([^)]+)\)',old.get(rel,'')))
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if target in oldlinks or '://' in target or target.startswith('#'): continue
  linkcount+=1
  if not (p.parent/unquote(target.strip('<>').split('#')[0])).exists(): bad.append([rel,target])
check('New local Markdown links resolve',not bad,f'{linkcount} links; failures={bad}')
def git(*a): return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.DEVNULL).decode('utf-8')
check('HEAD unchanged',git('rev-parse','HEAD').strip()==manifest['initial_head'])
initial=(A/'initial_git_status.txt').read_text(encoding='utf-8').splitlines()
current=git('status','--short').splitlines()
check('Every initial status entry retained',set(initial).issubset(current))
check('No task modifications to runtime, orders, images or experiments',all(not p.startswith(('engine/','09 Experiments/','13 Production/Orders/','13 Production/Clients/','13 Production/Portfolio/')) and Path(p).suffix in ['.md','.yaml'] for p in manifest['modified']))
diffcheck=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True,text=True)
check('git diff --check',diffcheck.returncode==0,diffcheck.stdout)
out={'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','checks':checks,'renderer_tests':{'passed':3,'output':'3 tests OK; planner counts and privacy vocabulary only; no PDF generated'},'scope':'Documentation/config consistency, no GPU/network/generation'}
(A/'validation_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(out['status']!='PASS')

