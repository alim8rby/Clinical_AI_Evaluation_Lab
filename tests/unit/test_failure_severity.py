import unittest
from src.failure_analysis.models import FailureSeverity
from src.failure_analysis.severity import assign_severity


class FailureSeverityTests(unittest.TestCase):
    def test_safety_output_escalates_at_half(self):
        self.assertEqual(
            assign_severity("SAFETY", "Potentially unsafe output", 0.49),
            FailureSeverity.HIGH,
        )
        self.assertEqual(
            assign_severity("SAFETY", "Potentially unsafe output", 0.50),
            FailureSeverity.CRITICAL,
        )

    def test_taxonomy_rules(self):
        self.assertEqual(assign_severity("RETRIEVAL", "Ranking failure", 0.2), FailureSeverity.LOW)
        self.assertEqual(assign_severity("RETRIEVAL", "Missing evidence", 0.0), FailureSeverity.MEDIUM)
        self.assertEqual(assign_severity("GENERATION", "Hallucination", 0.8), FailureSeverity.HIGH)
        self.assertEqual(assign_severity("CITATION", "Wrong citation", 0.5), FailureSeverity.HIGH)
        self.assertEqual(assign_severity("SYSTEM", "Invalid output", None), FailureSeverity.HIGH)

    def test_unknown_rule_has_safe_default(self):
        self.assertEqual(
            assign_severity("UNKNOWN", "Unknown failure", None),
            FailureSeverity.MEDIUM,
        )
