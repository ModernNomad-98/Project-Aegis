"""Synthetic, offline contract tests."""

import copy
import unittest

from tools.aegis_setup.routing_contract import (
    ContractError, FakeAdapter, check_compatibility, decide, parse_request,
)


def request_data():
    return {
        "version": "1", "synopsis": "Review a bounded API change", "stage": "review",
        "catalog_version": "cat-1", "policy_version": "pol-1",
        "agents": [{"id": "reviewer", "description": "Reviews code", "read_only": True},
                   {"id": "architect", "description": "Reviews design", "read_only": True}],
        "skills": [{"id": "api", "description": "API review", "manual_only": False},
                   {"id": "setup", "description": "Setup conversation", "manual_only": True}],
        "mandatory_agents": ["reviewer"], "mandatory_skills": [],
        "selected_agents": [], "selected_skills": [], "invoked_manual_skills": [],
    }


def response(**changes):
    value = {"version": "1", "catalog_version": "cat-1", "policy_version": "pol-1",
             "status": "recommend", "agents": ["reviewer"], "skills": ["api"], "score": None}
    value.update(changes)
    return value


class RoutingContractTests(unittest.TestCase):
    def setUp(self):
        self.request = parse_request(request_data())

    def test_valid_subset_and_abstain(self):
        result = FakeAdapter(response()).advise(self.request)
        self.assertEqual(result.disposition, "recommend")
        self.assertEqual(result.agents, ("reviewer",))
        self.assertEqual(decide(self.request, response(status="abstain", agents=[], skills=[])).disposition, "abstain")

    def test_empty_offers_can_abstain(self):
        data = request_data()
        data.update(agents=[], skills=[], mandatory_agents=[])
        req = parse_request(data)
        self.assertEqual(decide(req, response(status="abstain", agents=[], skills=[])).disposition, "abstain")
        self.assertEqual(decide(req, response(agents=[], skills=[])).disposition, "invalid")

    def test_duplicate_and_unknown_ids_fail(self):
        for change in (response(agents=["reviewer", "reviewer"]), response(skills=["unknown"]),
                       response(agents=[])):
            result = decide(self.request, change)
            self.assertEqual(result.disposition, "invalid")
            self.assertEqual(result.agents, ())
        data = request_data()
        data["agents"].append(copy.deepcopy(data["agents"][0]))
        with self.assertRaises(ContractError):
            parse_request(data)

    def test_explicit_and_manual_only(self):
        data = request_data()
        data["selected_agents"] = ["architect"]
        data["selected_skills"] = ["setup"]
        with self.assertRaises(ContractError):
            parse_request(data)
        data["invoked_manual_skills"] = ["setup"]
        req = parse_request(data)
        self.assertEqual(decide(req, response()).disposition, "invalid")
        self.assertEqual(decide(req, response(agents=["reviewer", "architect"], skills=["setup"])).disposition, "recommend")
        self.assertEqual(decide(self.request, response(skills=["setup"])).disposition, "invalid")

    def test_missing_mandatory_skill_has_no_selection(self):
        data = request_data()
        data["mandatory_skills"] = ["api"]
        result = decide(parse_request(data), response(skills=[]))
        self.assertEqual(result.disposition, "invalid")
        self.assertEqual(result.agents, ())
        self.assertEqual(result.skills, ())

    def test_version_schema_and_bounds(self):
        self.assertEqual(decide(self.request, response(catalog_version="cat-0")).disposition, "invalid")
        self.assertEqual(decide(self.request, response(version=2)).disposition, "invalid")
        self.assertEqual(decide(self.request, '{"version":"1","version":"1"}').disposition, "invalid")
        self.assertEqual(decide(self.request, response(destination="https://example.invalid")).disposition, "invalid")
        self.assertEqual(decide(self.request, response(score=1.2)).disposition, "invalid")
        self.assertEqual(decide(self.request, b"{" + b" " * 1100 + b"}").disposition, "invalid")
        data = request_data()
        data["synopsis"] = "x" * 513
        with self.assertRaises(ContractError):
            parse_request(data)
        data["synopsis"] = "token: secret"
        with self.assertRaises(ContractError):
            parse_request(data)

    def test_timeout_unavailable_and_no_online_fallback(self):
        for failure in ("timeout", "unavailable"):
            result = FakeAdapter(response(), failure=failure).advise(self.request)
            self.assertEqual(result.disposition, failure)
            self.assertEqual(result.agents, ())
        self.assertEqual(FakeAdapter(response(fallback="online")).advise(self.request).disposition, "invalid")
        self.assertEqual(FakeAdapter(response(status="online")).advise(self.request).disposition, "invalid")

    def test_read_only_flag_cannot_be_changed_by_advice(self):
        self.assertTrue(self.request.agents[0].read_only)
        self.assertEqual(decide(self.request, response(read_only=False)).disposition, "invalid")
        self.assertFalse(hasattr(decide(self.request, response()), "dispatch"))

    def test_compatibility_facts(self):
        facts = {"contract_version": "1", "catalog_version": "cat-1", "policy_version": "pol-1",
                 "agent_ids": ["reviewer", "architect"], "skill_ids": ["api", "setup"]}
        self.assertEqual(check_compatibility(facts, self.request).status, "compatible")
        self.assertEqual(check_compatibility({**facts, "catalog_version": "cat-2"}, self.request).status, "unsupported")
        self.assertEqual(check_compatibility({}, self.request).status, "unknown")
        self.assertEqual(check_compatibility({**facts, "skill_ids": ["api"]}, self.request).status, "unsupported")
        facts["agent_ids"] = ["reviewer", "reviewer"]
        self.assertEqual(check_compatibility(facts, self.request).status, "unknown")


if __name__ == "__main__":
    unittest.main()
