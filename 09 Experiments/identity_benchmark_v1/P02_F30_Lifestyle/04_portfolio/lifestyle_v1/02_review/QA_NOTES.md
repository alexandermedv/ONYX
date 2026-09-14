# Lifestyle QA notes

Source mapping was visually inspected before copying. All ten numbered/scene-named
files match the intended environments; the original names are preserved in the mapping.
The following are assistant observations for a human reviewer, not scores or decisions.

| ID | Attention point |
|---|---|
| LIFE_01 | Hand at chin differs from both hands at cup/table in prompt; inspect fingers and cup contact. |
| LIFE_02 | Hand in pocket differs from a naturally swinging arm; inspect stride and bag strap. |
| LIFE_03 | Mug and loosely gathered hair match the home scene; barefoot detail is outside the visible framing. |
| LIFE_04 | Inspect book lettering, fingers and crossed-leg anatomy. |
| LIFE_05 | Glass was added to the pose; inspect fingers, glass stem and rear-three-quarter anatomy. |
| LIFE_06 | Open smile and off-camera reaction supply diversity; inspect teeth and hand at hair. |
| LIFE_07 | Hand at chin differs from two forearms resting on railing; inspect profile and rail contact. |
| LIFE_08 | Hand at hair differs from arm along sofa back; inspect folded leg and cup contact. |
| LIFE_09 | Suitcase and travel clothing distinguish it from business; inspect gait and handle. |
| LIFE_10 | Outdoor evening street replacement confirmed visually; inspect coat-hand relationship. |

LIFE_05 and LIFE_10 both use a rear-three-quarter dark-dress pose; social grids avoid
placing these close alternatives together. Full-series overview cards intentionally
show the set's scope; they are not proof of perfect pose diversity.

PNG verification and decode, dimensions/ratio, unique SHA256 and EXIF presence are in
`technical_qa.csv`. Near-duplicate detection was skipped because the existing repository
detector needs unavailable `cv2`; no new dependency was installed. No identity embedding
score is claimed. QA does not modify pixels.

No standalone old office-like LIFE_10 was identified among the P02 source inventory
or other repository filenames matching LIFE/lifestyle. Its superseded status is retained
as user-provided history with a null filename. Do not substitute a business image for it.
