from app.services.phi_detector import PHIDetector
from app.services.phi_validator import PHIValidator

CASES = [
    {
        "text": "Patient Marcus Whitfield lives in Boston.",
        "expected": {"PERSON", "LOCATION"},
    },
    {
        "text": "The patient was born on 14 March 1978.",
        "expected": {"DATE_TIME"},
    },
    {
        "text": "Patient record: MRN PCG-4471902.",
        "expected": {"MEDICAL_RECORD_NUMBER"},
    },
    {
        "text": "Account Number: AC-2026-123456.",
        "expected": {"ACCOUNT_NUMBER"},
    },
    {
        "text": "Health Plan Beneficiary Number: HP-2026-445566.",
        "expected": {"HEALTH_PLAN_BENEFICIARY_NUMBER"},
    },
    {
        "text": "Email marcus@example.com and phone 617-555-0182.",
        "expected": {"EMAIL_ADDRESS", "PHONE_NUMBER"},
    },
]


def main():
    detector = PHIDetector()
    validator = PHIValidator()

    true_positive = 0
    false_positive = 0
    false_negative = 0

    print("PHI DETECTION EVALUATION")
    print("=" * 60)

    for index, case in enumerate(CASES, start=1):
        results = validator.validate(
           detector.analyze(case["text"])
        )

        predicted = {
            result.entity_type
            for result in results
        }

        expected = case["expected"]

        tp = len(predicted & expected)
        fp = len(predicted - expected)
        fn = len(expected - predicted)

        true_positive += tp
        false_positive += fp
        false_negative += fn

        print(f"\nCase {index}")
        print(f"Expected : {sorted(expected)}")
        print(f"Detected : {sorted(predicted)}")
        print(f"TP={tp}, FP={fp}, FN={fn}")

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0.0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

    print("\n" + "=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)
    print(f"True Positives : {true_positive}")
    print(f"False Positives: {false_positive}")
    print(f"False Negatives: {false_negative}")
    print(f"Precision      : {precision:.4f}")
    print(f"Recall         : {recall:.4f}")
    print(f"F1 Score       : {f1:.4f}")


if __name__ == "__main__":
    main()