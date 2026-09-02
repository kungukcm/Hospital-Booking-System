"""
Test script to verify CEO and management information retrieval
"""
import os
import sys

sys.path.insert(0, r"c:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Thesis Project\AI Assistant")

from hospital_tools import search_hospital_information

# Test queries
test_queries = [
    "Who is the CEO of KUTRRH?",
    "Who are the board members?",
    "Who are the directors?",
    "Who are the deputy directors?",
    "What is the name of the board chairman?"
]

print("=" * 80)
print("TESTING MANAGEMENT INFORMATION RETRIEVAL")
print("=" * 80)

for query in test_queries:
    print(f"\n{'=' * 80}")
    print(f"QUERY: {query}")
    print(f"{'=' * 80}")
    
    result = search_hospital_information.invoke({"query": query})
    print(result)
    print()
