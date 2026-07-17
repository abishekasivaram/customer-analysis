import pytest
from backend.services.advisor.rule_engine import RuleEngine
from backend.services.advisor.confidence_engine import ConfidenceEngine
from backend.services.advisor.business_summary import BusinessSummaryEngine
from backend.services.advisor.recommendation_validator import RecommendationValidator

def test_rule_engine_loading():
    re = RuleEngine()
    assert re.get_threshold("engagement", "high") > 0
    assert re.get_threshold("congestion", "critical") > 0

def test_confidence_computation():
    ce = ConfidenceEngine()
    # 2 supporting metrics = +10, trend stable = 0
    conf = ce.compute_confidence(2, "stable")
    assert conf == 90.0

def test_store_health_calculation():
    re = RuleEngine()
    bs = BusinessSummaryEngine(re)
    metrics = {"store_congestion_index": 90, "customer_engagement_score": 30}
    dashboard = {"zones": [{"visitors": 0}, {"visitors": 0}]} # 2 dead zones
    
    # 100 - 20 (congestion) - 15 (engagement) - 10 (2 dead zones) = 55
    health_data = bs.generate_store_health(metrics, {}, dashboard)
    assert health_data["store_health_score"] == 55.0

def test_recommendation_validator():
    rv = RecommendationValidator()
    invalid_rec = {"title": "Test"}
    assert not rv.validate(invalid_rec)
