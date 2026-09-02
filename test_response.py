"""Test what the hospital tool is returning"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import sys
sys.path.insert(0, r"C:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Thesis Project\AI Assistant")

from hospital_tools import search_hospital_information

# Test the exact query
query = "What are the payment methods?"
print(f"Testing query: '{query}'")
print("="*70)

result = search_hospital_information(query)

print(f"\nResponse:")
print(result)
print("="*70)
