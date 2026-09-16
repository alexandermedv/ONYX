from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
RULE='Use MASTER and REF01–REF05 strictly for facial identity, facial structure, natural body proportions, skin tone, apparent age, hair characteristics and mature executive appearance only. Do NOT mechanically copy pose, head angle, gaze, expression, hand placement, composition, clothing or hairstyle arrangement. Create genuinely different photographs of the same man.'
SCENES=[
('EXEC_01','P03_EXEC_01_headshot_front.png','Premium front-facing executive headshot; head and shoulders, direct eye contact, dark navy suit, ivory shirt, calm confident intelligent expression, soft modern office background and natural window light.'),
('EXEC_02','P03_EXEC_02_window_3q.png','Waist-up portrait beside a floor-to-ceiling window; torso 30–40 degrees, charcoal suit, city background, restrained expression, directional daylight, one hand naturally adjusting cuff or jacket.'),
('EXEC_03','P03_EXEC_03_executive_desk.png','Seated at a premium executive desk, mid-thigh or waist-up, neutral jacket, notebook and laptop, engaged posture, gaze off camera and focused expression.'),
('EXEC_04','P03_EXEC_04_office_walk.png','Knees-up or near-full-body mid-stride through a modern glass office corridor, slim laptop case, purposeful gaze away from camera, subtle motion.'),
('EXEC_05','P03_EXEC_05_boardroom.png','Standing beside a glass and wood conference table in a dark green, navy or charcoal suit, one hand naturally on chair or table, upright authoritative posture and serious direct gaze.'),
('EXEC_06','P03_EXEC_06_lobby_fullbody.png','Premium full-body portrait in a luxury business lobby, taupe or gray suit, elegant shoes, natural asymmetrical stance, one hand holding a folio, slight professional smile.'),
('EXEC_07','P03_EXEC_07_private_office.png','Seated sideways in a dark wood private office, body side-on and face turned back, thoughtful serious expression, document or book in hand.'),
('EXEC_08','P03_EXEC_08_laptop_workspace.png','Candid working moment in a bright collaborative workspace, open laptop, executive-casual wardrobe, looking at screen, both hands natural, spontaneous workday expression.'),
('EXEC_09','P03_EXEC_09_window_profile.png','Mostly side profile by a window, looking outside rather than at camera, arms loosely crossed or hands resting, cinematic strategic expression, city softly blurred.'),
('EXEC_10','P03_EXEC_10_editorial_fullbody.png','Premium leadership editorial near full body in minimalist architectural office, sophisticated neutral suit, one leg forward, holding slim leather portfolio, chin slightly raised.')]
for d in ['00_source','01_prompts','02_review','03_final','04_web/jpg','04_web/webp','05_marketing/01_contact_sheet','05_marketing/02_avito_carousel','05_marketing/03_before_after','05_marketing/04_social','05_marketing/05_copy']:(ROOT/d).mkdir(parents=True,exist_ok=True)
for ident,fn,p in SCENES:(ROOT/'01_prompts'/f'{ident}.txt').write_text(RULE+'\n\n'+p+'\n\nPhotorealistic premium executive editorial photography. One adult synthetic man only, natural anatomy, no text, logo or watermark. Avoid identity drift, distorted hands, extra or missing limbs.\n',encoding='utf-8')
(ROOT/'01_prompts'/'P03_executive_v1_prompts.md').write_text('# P03 Executive v1 prompts\n\n'+RULE+'\n\n'+'\n\n'.join(f'## {i}\n\n{p}' for i,_,p in SCENES)+'\n',encoding='utf-8')
(ROOT/'01_prompts'/'P03_executive_v1_prompts.yaml').write_text(json.dumps({'session_id':'P03_EXECUTIVE_V1','session_rule':RULE,'scenes':[{'id':i,'filename':f,'prompt':p} for i,f,p in SCENES]},indent=2)+'\n',encoding='utf-8')
(ROOT/'GENERATION_STATUS.md').write_text('# P03 Executive v1 generation status\n\n'+''.join(f'- {i}: MISSING — queued for sequential generation\n' for i,_,_ in SCENES),encoding='utf-8')
