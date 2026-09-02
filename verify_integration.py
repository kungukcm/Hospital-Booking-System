#!/usr/bin/env python
"""
Verify TCN scheduling model integration
Tests model loading, agent initialization, and tool functionality
"""

import sys
import os
from datetime import datetime, timedelta

def verify_model_loading():
    """Verify TCN model loads correctly"""
    print("\n✓ Testing Model Loading...")
    try:
        from scheduling_model import SchedulingPredictor
        
        predictor = SchedulingPredictor(
            model_path='models/tcn_scheduling_model.h5',
            framework='tensorflow'
        )
        
        assert not predictor.use_mock, "Model should be loaded, not using mock"
        assert predictor.framework == 'tensorflow', "Framework should be TensorFlow"
        print("  ✓ Model loaded successfully (TensorFlow)")
        print(f"  ✓ Model path: {predictor.model_path}")
        print(f"  ✓ Using real predictions: {not predictor.use_mock}")
        return True
    except Exception as e:
        print(f"  ✗ Model loading failed: {e}")
        return False

def verify_enhanced_tools():
    """Verify enhanced tools initialize correctly"""
    print("\n✓ Testing Enhanced Tools...")
    try:
        from enhanced_tools import init_predictor
        
        p = init_predictor()
        assert p is not None, "Predictor should be initialized"
        assert not p.use_mock, "Should use real model, not mock"
        print("  ✓ Enhanced tools initialized")
        print(f"  ✓ Predictor initialized with real model")
        return True
    except Exception as e:
        print(f"  ✗ Enhanced tools initialization failed: {e}")
        return False

def verify_agent():
    """Verify agent loads with ML-enhanced tools"""
    print("\n✓ Testing Agent Workflow...")
    try:
        from agent import caller_app, caller_tools
        
        assert caller_app is not None, "Agent should be compiled"
        assert len(caller_tools) == 7, f"Should have 7 tools, got {len(caller_tools)}"
        
        tool_names = [t.name for t in caller_tools]
        expected_tools = [
            'book_appointment',
            'get_next_available_appointment',
            'get_optimal_appointment_slots',
            'get_wait_time_prediction',
            'get_busiest_times',
            'get_least_busy_times',
            'cancel_appointment'
        ]
        
        for expected in expected_tools:
            assert expected in tool_names, f"Missing tool: {expected}"
        
        print(f"  ✓ Agent compiled successfully")
        print(f"  ✓ Number of tools: {len(caller_tools)}")
        print(f"  ✓ Tools: {', '.join(tool_names)}")
        return True
    except Exception as e:
        print(f"  ✗ Agent verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_predictions():
    """Verify model makes real predictions"""
    print("\n✓ Testing Model Predictions...")
    try:
        from scheduling_model import SchedulingPredictor
        
        predictor = SchedulingPredictor(
            model_path='models/tcn_scheduling_model.h5',
            framework='tensorflow'
        )
        
        # Test waiting time prediction
        test_time = datetime.now() + timedelta(days=1)
        wait_time, confidence = predictor.predict_waiting_time('consultation', test_time)
        
        assert wait_time > 0, "Waiting time should be positive"
        assert 0 <= confidence <= 1, "Confidence should be between 0 and 1"
        
        print(f"  ✓ Waiting time prediction: {wait_time:.1f} min (confidence: {confidence*100:.0f}%)")
        
        # Test optimal slot recommendations
        slots = predictor.recommend_optimal_slots('consultation', test_time.date(), num_recommendations=3)
        
        assert len(slots) > 0, "Should return at least one recommended slot"
        assert all('time' in slot for slot in slots), "All slots should have time"
        assert all('predicted_wait_minutes' in slot for slot in slots), "All slots should have predictions"
        
        print(f"  ✓ Recommended {len(slots)} optimal appointment slots")
        for slot in slots[:3]:
            print(f"    - {slot['time']}: {slot['predicted_wait_minutes']:.0f} min estimated wait")
        
        return True
    except Exception as e:
        print(f"  ✗ Prediction verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 70)
    print("TCN Scheduling Model Integration Verification")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    results = {
        "Model Loading": verify_model_loading(),
        "Enhanced Tools": verify_enhanced_tools(),
        "Agent Workflow": verify_agent(),
        "Model Predictions": verify_predictions()
    }
    
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    print("=" * 70)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ TCN integration verified successfully!")
        print("\nNext steps:")
        print("1. Test locally: streamlit run app.py")
        print("2. Push to GitHub: git push origin main")
        print("3. Streamlit Cloud will auto-deploy")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
