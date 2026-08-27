from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.api.database import get_db
from backend.api.models import Prediction

router_stats = APIRouter(prefix="/stats", tags=["Statistiques"])

@router_stats.get("/")
def get_stats(db: Session = Depends(get_db)):
    """
    Retourne les statistiques globales des prédictions.
    """
    total = db.query(Prediction).count()
    
    avg_confidence = db.query(
        func.avg(Prediction.confidence)
    ).scalar()

    most_common = db.query(
        Prediction.waste_class,
        func.count(Prediction.waste_class).label("count")
    ).group_by(
        Prediction.waste_class
    ).order_by(
        func.count(Prediction.waste_class).desc()
    ).first()

    return {
        "total_predictions": total,
        "average_confidence": round(float(avg_confidence), 2) if avg_confidence else 0.0,
        "most_common_class": most_common[0] if most_common else "aucune",
        "most_common_count": most_common[1] if most_common else 0
    }

@router_stats.get("/by-class")
def get_stats_by_class(db: Session = Depends(get_db)):
    """
    Retourne les statistiques par classe de déchet.
    """
    results = db.query(
        Prediction.waste_class,
        func.count(Prediction.waste_class).label("count"),
        func.avg(Prediction.confidence).label("avg_confidence")
    ).group_by(
        Prediction.waste_class
    ).all()

    return [
        {
            "waste_class": r[0],
            "count": r[1],
            "avg_confidence": round(float(r[2]), 2)
        }
        for r in results
    ]