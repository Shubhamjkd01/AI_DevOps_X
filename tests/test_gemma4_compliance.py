"""
Gemma 4 Compliance and Verification Test Suite.
Asserts that only open-weight Gemma 4 models are called, and no non-Gemma models are ever invoked.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm import query_llm, _try_gemma, get_last_model_used, GEMMA4_CANDIDATES


class TestGemma4Compliance(unittest.TestCase):

    def setUp(self):
        # Set dummy key for mock tests
        os.environ["GEMMA_API_KEY"] = "mock_test_key_gemma4"
        os.environ["GEMMA_MODEL_NAME"] = "models/gemma-4-26b-a4b-it"
        os.environ["TEST_MODE"] = "false"

    def test_gemma_candidates_only_contain_gemma_4(self):
        """Verify candidate list contains only Gemma 4 models and no Gemini/closed models."""
        for model in GEMMA4_CANDIDATES:
            self.assertIn("gemma-4", model.lower(), f"Non-Gemma-4 model found in candidates: {model}")
            self.assertNotIn("gemini-1.5", model.lower())
            self.assertNotIn("gemma-2", model.lower())
            self.assertNotIn("gpt", model.lower())

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_assert_no_non_gemma_model_called(self, mock_configure, mock_model_cls):
        """Assert that GenerativeModel is only called with Gemma 4 models."""
        called_models = []

        def side_effect(model_name):
            called_models.append(model_name)
            mock_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Gemma 4 response"
            mock_instance.generate_content.return_value = mock_response
            return mock_instance

        mock_model_cls.side_effect = side_effect

        text, model_used = _try_gemma("Test prompt for Gemma 4")

        # Verify calls
        self.assertGreater(len(called_models), 0)
        for model in called_models:
            self.assertIn("gemma-4", model.lower(), f"Violation: Non-Gemma model called: {model}")
            self.assertNotIn("gemini", model.lower().replace("models/", ""))
            self.assertNotIn("gpt", model.lower())

        self.assertIn("gemma-4", model_used.lower())
        self.assertEqual(text, "Gemma 4 response")

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_query_llm_records_model_used(self, mock_configure, mock_model_cls):
        """Verify query_llm logs and exposes model_used attribute and context."""
        mock_instance = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = "Fixed syntax error on line 42"
        mock_instance.generate_content.return_value = mock_resp
        mock_model_cls.return_value = mock_instance

        res = query_llm("Fix code")

        self.assertEqual(res, "Fixed syntax error on line 42")
        self.assertTrue(hasattr(res, "model_used"))
        self.assertIn("gemma-4", res.model_used.lower())
        self.assertEqual(get_last_model_used(), res.model_used)

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_aborts_without_opening_pr_if_gemma_fails(self, mock_configure, mock_model_cls):
        """Verify pipeline aborts with RuntimeError when Gemma fails and TEST_MODE=false."""
        os.environ["TEST_MODE"] = "false"
        # Force Gemma failure
        mock_instance = MagicMock()
        mock_instance.generate_content.side_effect = Exception("API rate limit exceeded")
        mock_model_cls.return_value = mock_instance

        with self.assertRaises(RuntimeError) as ctx:
            query_llm("Analyze critical CI log")

        self.assertIn("Aborting pipeline without opening a PR", str(ctx.exception))

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_test_mode_permits_mock_response(self, mock_configure, mock_model_cls):
        """Verify TEST_MODE=true safely permits offline mock response without crashing."""
        os.environ["TEST_MODE"] = "true"
        mock_instance = MagicMock()
        mock_instance.generate_content.side_effect = Exception("API connection offline")
        mock_model_cls.return_value = mock_instance

        res = query_llm("Fix syntax")
        self.assertIn("mock-test-mode", res.model_used)
        self.assertTrue(len(res) > 0)


if __name__ == "__main__":
    unittest.main()
