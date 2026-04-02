import pytest
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from model import predict
from decision_engine import generate_decision
from event_detector import detect_event
from impact_model import map_impact
from nlp_engine import extract_locations


class TestPredictModel:
    """Test cases for the prediction model"""
    
    def test_predict_with_positive_sentiments(self):
        """Test prediction with positive sentiments"""
        sentiments = [
            {"label": "POSITIVE", "score": 0.95},
            {"label": "POSITIVE", "score": 0.87},
        ]
        prediction, confidence = predict(sentiments)
        
        assert prediction is not None
        assert confidence > 0
        assert all(asset in prediction for asset in ["gold", "silver", "oil"])
    
    def test_predict_with_negative_sentiments(self):
        """Test prediction with negative sentiments"""
        sentiments = [
            {"label": "NEGATIVE", "score": -0.95},
            {"label": "NEGATIVE", "score": -0.87},
        ]
        prediction, confidence = predict(sentiments)
        
        assert prediction is not None
        assert confidence < 0
        assert all(asset in prediction for asset in ["gold", "silver", "oil"])
    
    def test_predict_with_mixed_sentiments(self):
        """Test prediction with mixed sentiments"""
        sentiments = [
            {"label": "POSITIVE", "score": 0.8},
            {"label": "NEGATIVE", "score": -0.6},
        ]
        prediction, confidence = predict(sentiments)
        
        assert prediction is not None
        assert all(asset in prediction for asset in ["gold", "silver", "oil"])
    
    def test_predict_with_empty_list(self):
        """Test prediction with empty sentiment list"""
        prediction, confidence = predict([])
        
        assert prediction is not None
        assert confidence == 0.0
        assert all(action == "HOLD" for action in prediction.values())
    
    def test_predict_with_none(self):
        """Test prediction with None"""
        prediction, confidence = predict(None)
        
        assert prediction is not None
        assert confidence == 0.0


class TestDecisionEngine:
    """Test cases for decision generation"""
    
    def test_generate_decision_buy(self):
        """Test decision generation for BUY signal"""
        prediction = {"gold": "BUY", "silver": "BUY", "oil": "BUY"}
        confidence = 0.85
        
        decisions = generate_decision(prediction, confidence)
        
        assert decisions is not None
        assert decisions["gold"]["action"] == "BUY"
        assert decisions["gold"]["confidence"] == 85.0
        assert decisions["gold"]["status"] == "ACTIVE"
    
    def test_generate_decision_sell(self):
        """Test decision generation for SELL signal"""
        prediction = {"gold": "SELL", "silver": "SELL", "oil": "SELL"}
        confidence = -0.75
        
        decisions = generate_decision(prediction, confidence)
        
        assert decisions is not None
        assert decisions["gold"]["action"] == "SELL"
        assert decisions["gold"]["confidence"] == 75.0
    
    def test_generate_decision_hold(self):
        """Test decision generation for HOLD signal"""
        prediction = {"gold": "HOLD", "silver": "HOLD", "oil": "HOLD"}
        confidence = 0.1
        
        decisions = generate_decision(prediction, confidence)
        
        assert decisions is not None
        assert decisions["gold"]["action"] == "HOLD"
        assert decisions["gold"]["confidence"] == 10.0
    
    def test_generate_decision_empty_prediction(self):
        """Test decision generation with empty prediction"""
        decisions = generate_decision({}, 0.5)
        
        assert decisions is not None
        assert len(decisions) == 0


class TestEventDetector:
    """Test cases for event detection"""
    
    def test_detect_geopolitical_event(self):
        """Test geopolitical event detection"""
        assert detect_event("War breaks out in the Middle East") == "GEOPOLITICAL"
        assert detect_event("Military conflict reported") == "GEOPOLITICAL"
        assert detect_event("Ongoing conflict in Ukraine") == "GEOPOLITICAL"
    
    def test_detect_inflation_event(self):
        """Test inflation event detection"""
        assert detect_event("Inflation rises to 5%") == "INFLATION"
        assert detect_event("Price surge in commodities") == "INFLATION"
    
    def test_detect_interest_rate_event(self):
        """Test interest rate event detection"""
        assert detect_event("Fed raises interest rates") == "INTEREST_RATE"
        assert detect_event("Central bank decision on rates") == "INTEREST_RATE"
    
    def test_detect_oil_market_event(self):
        """Test oil market event detection"""
        assert detect_event("Oil prices jump 5%") == "OIL_MARKET"
        assert detect_event("Crude oil exports halted") == "OIL_MARKET"
        assert detect_event("Energy crisis reported") == "OIL_MARKET"
    
    def test_detect_general_event(self):
        """Test general event detection"""
        assert detect_event("Stock market reaches new high") == "GENERAL"
        assert detect_event("Economic growth slows") == "GENERAL"
    
    def test_detect_event_empty_text(self):
        """Test event detection with empty text"""
        assert detect_event("") == "GENERAL"
        assert detect_event(None) == "GENERAL"


class TestImpactModel:
    """Test cases for impact mapping"""
    
    def test_impact_geopolitical(self):
        """Test impact mapping for geopolitical events"""
        impact = map_impact("GEOPOLITICAL")
        
        assert impact is not None
        assert impact.get("gold") == "BUY"
        assert impact.get("oil") == "BUY"
    
    def test_impact_inflation(self):
        """Test impact mapping for inflation events"""
        impact = map_impact("INFLATION")
        
        assert impact is not None
        assert impact.get("gold") == "BUY"
        assert impact.get("silver") == "BUY"
    
    def test_impact_interest_rate(self):
        """Test impact mapping for interest rate events"""
        impact = map_impact("INTEREST_RATE")
        
        assert impact is not None
        assert impact.get("gold") == "SELL"
        assert impact.get("silver") == "SELL"
    
    def test_impact_oil_market(self):
        """Test impact mapping for oil market events"""
        impact = map_impact("OIL_MARKET")
        
        assert impact is not None
        assert impact.get("oil") == "BUY"
    
    def test_impact_general(self):
        """Test impact mapping for general events"""
        impact = map_impact("GENERAL")
        
        assert impact is not None
        assert impact.get("gold") == "HOLD"


class TestNLPEngine:
    """Test cases for NLP engine"""
    
    def test_extract_locations_single(self):
        """Test location extraction with single location"""
        locations = extract_locations("War in Ukraine affects gold prices")
        
        assert locations is not None
        assert "ukraine" in [loc.lower() for loc in locations]
    
    def test_extract_locations_multiple(self):
        """Test location extraction with multiple locations"""
        text = "Conflict between USA and China impacts oil market"
        locations = extract_locations(text)
        
        assert locations is not None
        assert len(locations) > 0
    
    def test_extract_locations_none(self):
        """Test location extraction with no locations"""
        locations = extract_locations("Stock market reports positive growth")
        
        assert locations is not None
        assert len(locations) == 0
    
    def test_extract_locations_empty(self):
        """Test location extraction with empty text"""
        locations = extract_locations("")
        
        assert locations is not None
        assert len(locations) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
