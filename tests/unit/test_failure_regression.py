import unittest

from src.failure_analysis.models import FailureSeverity
from src.failure_analysis.regression import (
    RegressionCase,
    assert_regression_suite,
    default_regression_cases,
    run_regression_suite,
)


class FailureRegressionTests(unittest.TestCase):
    def test_default_suite_passes_current_severity_rules(self):
        results = run_regression_suite()
        self.assertEqual(len(results), len(default_regression_cases()))
        self.assertTrue(all(result.passed for result in results))

    def test_assertion_passes_for_current_implementation(self):
        assert_regression_suite()

    def test_regression_suite_detects_rule_change(self):
        def broken_assigner(category, failure_type, metric_value):
            return FailureSeverity.LOW

        results = run_regression_suite(assigner=broken_assigner)
        self.assertTrue(any(not result.passed for result in results))

    def test_case_validation_rejects_empty_id(self):
        with self.assertRaises(ValueError):
            RegressionCase("", "GENERATION", "Hallucination", 0.75, FailureSeverity.HIGH)

    def test_unsafe_threshold_is_covered(self):
        cases = default_regression_cases()
        high = next(case for case in cases if case.case_id == "safety-unsafe-high")
        low = next(case for case in cases if case.case_id == "safety-unsafe-low")
        self.assertEqual(high.metric_value, 0.5)
        self.assertEqual(low.metric_value, 0.25)
