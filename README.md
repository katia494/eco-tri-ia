# ECO-TRI IA

Application web de tri des dÃ©chets par vision artificielle.

Une interface React/Vite envoie une image Ã  une API FastAPI. Le modÃ¨le
**YOLOv8n-cls V3** classe lâ€™objet parmi six catÃ©gories, puis lâ€™application
retourne la classe, le niveau de confiance et une consigne de tri. Les images
envoyÃ©es par lâ€™utilisateur ne sont pas conservÃ©es.

## RÃ©sultats vÃ©rifiÃ©s

| Ã‰valuation | Images | Accuracy | Macro F1 | InterprÃ©tation |
|---|---:|---:|---:|---|
| V3 interne | 793 | **93,69 %** | **92,87 %** | Performance sur le pÃ©rimÃ¨tre proche de lâ€™entraÃ®nement |
| V3 sur ancien test V2 verrouillÃ© | 383 | **88,51 %** | **87,00 %** | Comparaison contrÃ´lÃ©e avec le modÃ¨le prÃ©cÃ©dent |
| V3 externe RealWaste | 3 587 | **41,96 %** | **40,98 %** | GÃ©nÃ©ralisation limitÃ©e hors pÃ©rimÃ¨tre dâ€™entraÃ®nement |

Le modÃ¨le fournit six classes : `cardboard`, `glass`, `metal`, `paper`,
`plastic` et `trash`.

Lâ€™Ã©valuation RealWaste est volontairement sÃ©parÃ©e de lâ€™entraÃ®nement. Elle
montre quâ€™ECO-TRI IA est un prototype pÃ©dagogique utile pour le pÃ©rimÃ¨tre
appris, mais ne doit pas Ãªtre prÃ©sentÃ© comme un systÃ¨me de tri municipal
gÃ©nÃ©ralisable.

## DonnÃ©es et qualitÃ©

- Catalogue SQLite : **7 769 images canoniques** et **9 985 liens de provenance**.
- Sources dâ€™entraÃ®nement documentÃ©es : Garbage Classification V1 et V2.
- RealWaste est rÃ©servÃ© Ã  lâ€™Ã©valuation externe.
- Les doublons sont dÃ©tectÃ©s par SHA-256 ; les exclusions sont versionnÃ©es.
- Le modÃ¨le final est `yolov8n-cls-v3`.

## QualitÃ© logicielle

- **46 tests Pytest rÃ©ussis** ;
- **89 % de couverture backend** ;
- CI GitHub Actions exÃ©cutÃ©e Ã  chaque push ;
- validation locale du build Docker et de la route `/health`.

## Architecture

```text
Utilisateur â†’ React/Vite â†’ FastAPI â†’ YOLOv8n-cls V3
                              â”œâ”€ SQLite : catalogue et prÃ©dictions
                              â”œâ”€ API de donnÃ©es protÃ©gÃ©e par clÃ©
                              â””â”€ logs, mÃ©triques et monitoring


## FonctionnalitÃ©s

- import ou capture dâ€™une image JPG/PNG ;
- validation du type, du contenu et de la taille de lâ€™image ;
- prÃ©diction parmi les six catÃ©gories ;
- affichage de la confiance et dâ€™une consigne de tri ;
- seuil dâ€™incertitude configurÃ© Ã  60 % ;
- historique et statistiques des prÃ©dictions ;
- points de collecte associÃ©s Ã  la catÃ©gorie ;
- monitoring sur `/stats/monitoring` ;
- documentation OpenAPI sur `/docs`.

## Installation locale

PrÃ©requis : Python 3.12 et Node.js 22.

```powershell
git clone https://github.com/katia494/eco-tri-ia.git
cd eco-tri-ia
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.api.main:app --reload
