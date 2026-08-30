from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.api.database import get_db
from backend.api.models import Prediction
from backend.api.config import settings
from backend.api.monitoring import monitoring_registry

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


@router_stats.get("/monitoring", tags=["Monitoring"])
def get_monitoring(db: Session = Depends(get_db)):
    """Expose les métriques applicatives et IA utiles au diagnostic du MVP."""
    total_predictions = db.query(Prediction).count()
    uncertain_predictions = db.query(Prediction).filter(
        Prediction.confidence < settings.confidence_threshold
    ).count()
    uncertain_rate = (
        uncertain_predictions / total_predictions if total_predictions else 0.0
    )

    return {
        "application": monitoring_registry.snapshot(),
        "model": {
            "version": settings.model_version,
            "confidence_threshold": settings.confidence_threshold,
            "prediction_count": total_predictions,
            "uncertain_prediction_count": uncertain_predictions,
            "uncertain_prediction_rate": round(uncertain_rate, 4),
        },
        "alert_thresholds": {
            "error_rate": 0.05,
            "latency_ms": 2000,
            "uncertain_prediction_rate": 0.20,
        },
    }
