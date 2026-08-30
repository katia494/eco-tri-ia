# Guide de déploiement

## Développement local

```bash
python -m venv .venv
```

Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.api.main:app --reload
```

Frontend :

```bash
cd frontend
npm ci
npm run dev
```

## Vérification avant livraison

```bash
pytest tests/ -v --cov=backend --cov-report=term-missing
cd frontend
npm run lint
npm run build
```

## Docker

```bash
docker compose build
docker compose up -d
curl http://localhost:8000/health
```

Tester ensuite `/docs`, `/model/info`, une image valide, un fichier texte et les
statistiques. Ne pas créer de release si l'un de ces contrôles échoue.

## Variables

| Variable | Valeur par défaut | Rôle |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./data/eco_tri.db` | Stockage SQLite local unique |
| `MODEL_PATH` | `backend/models/best.pt` | Modèle final |
| `MODEL_VERSION` | `yolov8n-cls-v1` | Traçabilité |
| `MAX_UPLOAD_BYTES` | `10485760` | Limite d'upload |
