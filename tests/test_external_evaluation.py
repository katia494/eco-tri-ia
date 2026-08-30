from scripts.evaluate_external_dataset import CLASSES, compute_report


def test_external_report_calculates_accuracy_f1_and_uncertainty():
    records = []
    for class_name in CLASSES:
        records.append(
            {
                "expected_class": class_name,
                "predicted_class": class_name,
                "confidence": 0.90,
            }
        )
    records[0]["predicted_class"] = "paper"
    records[0]["confidence"] = 0.52

    report = compute_report(records, threshold=0.60)

    assert report["test_images"] == 6
    assert report["accuracy"] == 0.8333
    assert report["uncertain_predictions"] == 1
    assert report["uncertain_rate"] == 0.1667
    assert report["error_count"] == 1
