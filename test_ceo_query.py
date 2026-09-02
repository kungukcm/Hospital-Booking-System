#!/usr/bin/env python3
"""Regression checks for exact leadership role queries."""

from hospital_tools import search_hospital_information


def expect_contains(query: str, *must_contain):
    result = search_hospital_information.invoke({"query": query})
    text = result.lower()
    for needle in must_contain:
        assert needle.lower() in text, f"Query: {query}\nResult: {result}\nMissing: {needle}"
    return result


print("=== Testing exact leadership-role queries ===\n")

# Clinical Services Director must resolve to the single named role, not the whole executive list.
result = expect_contains(
    "Who is the director of clinical services?",
    "dr. anthony kamau",
    "director, clinical services"
)
print(f"Result: {result}\n")

# CEO query should still resolve to Dr. Zeinab Gura, not the whole executive list.
result = expect_contains(
    "Who is the CEO of KUTRRH?",
    "dr. zeinab gura",
    "chief executive officer"
)
print(f"Result: {result}\n")
