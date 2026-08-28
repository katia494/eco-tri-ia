# Benchmark des services IA – ECO-TRI

> **Auteure** : Katia Boussad – Formation Dev IA, Simplon  
> **Date** : Août 2026

---

## 1. Besoin reformulé

Classer automatiquement des images de déchets en 6 catégories :
cardboard, glass, metal, paper, plastic, trash.

**Contraintes** : gratuit, local, rapide, sans données personnelles.

---

## 2. Services et modèles étudiés
Service	Fonctionnel	Technique	Coût	Risque	Décision
Scikit-learn (Random Forest)	✅ Fort	✅ Simple	✅ Gratuit	✅ Faible	✅ RETENU
YOLOv8 (Ultralytics)	✅ Fort	⚠️ Complexe	✅ Gratuit	⚠️ Moyen	❌ Écarté
Google Vision API	✅ Très fort	✅ Simple	❌ Payant	❌ Cloud	❌ Écarté
AWS Rekognition	✅ Très fort	⚠️ Moyen	❌ Payant	❌ Cloud	❌ Écarté
TensorFlow CNN	✅ Fort	❌ Complexe	✅ Gratuit	⚠️ Moyen	❌ Écarté


3. Pourquoi on a écarté les autres
YOLOv8 → Trop complexe à intégrer dans le délai du projet.
Prévu pour la détection d'objets en temps réel, pas optimal
pour la classification simple sur 6 catégories.

Google Vision API → Service cloud payant.
Les images seraient envoyées vers les serveurs Google
→ problème RGPD + coût incompatible avec le budget.

AWS Rekognition → Même problème que Google Vision.
Payant, cloud, données envoyées hors de France.

TensorFlow CNN → Trop long à entraîner et à configurer
pour le délai disponible. Surpuissant pour notre dataset de 2527 images.

4. Pourquoi on a retenu Scikit-learn
✅ Gratuit et open source
✅ Local — aucune donnée envoyée sur internet
✅ Rapide à entraîner (quelques secondes)
✅ Documenté — documentation officielle claire
✅ Conforme RGPD — pas de cloud, pas de fuite de données
✅ 94% de précision sur notre dataset


5. Résultat du test minimal
bash
Copy
python src/collecte_donnees.py
→ 2527 images collectées ✅

python src/import_data.py  
→ Base de données créée ✅

uvicorn backend.api.main:app --reload
→ API démarrée sur http://localhost:8000 ✅

GET http://localhost:8000/health
→ {"status": "ok", "message": "ECO-TRI API is running"} ✅

6. Conclusion
Scikit-learn Random Forest est le choix optimal pour ECO-TRI :
simple, gratuit, local, performant et conforme RGPD.
