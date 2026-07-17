import json
from backend.services.advisor.layout_optimizer import LayoutOptimizer
from backend.services.advisor.inventory_advisor import InventoryAdvisor
from backend.services.advisor.engagement_advisor import EngagementAdvisor
from backend.services.advisor.flow_optimizer import FlowOptimizer
from backend.services.advisor.recommendation_validator import RecommendationValidator
from backend.core.logger import rec_logger

class RecommendationGenerator:
    def __init__(self, rule_engine, confidence_engine):
        self.rule_engine = rule_engine
        self.conf_engine = confidence_engine
        self.layout_opt = LayoutOptimizer(rule_engine, confidence_engine)
        self.inv_adv = InventoryAdvisor(rule_engine, confidence_engine)
        self.eng_adv = EngagementAdvisor(rule_engine, confidence_engine)
        self.flow_opt = FlowOptimizer(rule_engine, confidence_engine)
        self.validator = RecommendationValidator()

    def generate(self, dashboard_data, trends, flow_data):
        rec_logger.info("Starting recommendation generation...")
        recs = []
        
        recs.extend(self.layout_opt.analyze(dashboard_data, trends))
        recs.extend(self.inv_adv.analyze(dashboard_data, trends))
        recs.extend(self.eng_adv.analyze(dashboard_data, trends))
        recs.extend(self.flow_opt.analyze(flow_data, trends))
        
        # Deduplication
        recs = self._deduplicate(recs)
        
        # Validation
        valid_recs = []
        for r in recs:
            if self.validator.validate(r):
                valid_recs.append(r)
                
        # Ranking
        ranked_recs = self._rank(valid_recs)
        
        rec_logger.info(f"Generated {len(ranked_recs)} valid recommendations.")
        return ranked_recs
        
    def _deduplicate(self, recs):
        # Merge recommendations with same title and zone/category
        merged = {}
        for r in recs:
            key = (r['title'], r['category'])
            if key not in merged:
                r['supporting_rules'] = [r['triggered_rule']]
                r['rule_count'] = 1
                r['highest_confidence'] = r['confidence']
                merged[key] = r
            else:
                existing = merged[key]
                existing['supporting_rules'].append(r['triggered_rule'])
                existing['rule_count'] += 1
                existing['highest_confidence'] = max(existing['highest_confidence'], r['confidence'])
                existing['confidence'] = existing['highest_confidence']
        return list(merged.values())

    def _rank(self, recs):
        priority_map = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        # Sort by Priority -> Impact Score -> Confidence -> ROI
        # ROI simple map
        roi_map = {"High": 3, "Medium": 2, "Low": 1}
        
        return sorted(recs, key=lambda x: (
            priority_map.get(str(x.get('priority')).upper(), 0),
            x.get('impact_score', 0),
            x.get('confidence', 0),
            roi_map.get(str(x.get('estimated_roi')), 0)
        ), reverse=True)
