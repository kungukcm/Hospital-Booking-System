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

# Board chairperson query must resolve to the single chairperson, not a board list.
result = expect_contains(
    "Who is the board chairperson?",
    "mr. james kibugu wambu",
    "chairman of the board"
)
print(f"Result: {result}\n")

# Director of nursing should resolve to the named nursing director.
result = expect_contains(
    "Who is the Director of Nursing Services?",
    "dr. pamleila ntwiga",
    "director, nursing services"
)
print(f"Result: {result}\n")

# Swahili leadership queries should also resolve to the exact named individuals.
result = expect_contains(
    "Nani ni Mkurugenzi wa Huduma za Uuguzi?",
    "dr. pamleila ntwiga",
    "mkurugenzi wa huduma za uuguzi"
)
print(f"Result: {result}\n")

result = expect_contains(
    "Nani ni Mkurugenzi Mtendaji wa KUTRRH?",
    "dr. zeinab gura",
    "mkurugenzi mtendaji"
)
print(f"Result: {result}\n")

result = expect_contains(
    "Nani ni Mwenyekiti wa bodi?",
    "mr. james kibugu wambu",
    "mwenyekiti wa bodi"
)
print(f"Result: {result}\n")

# CEO query should still resolve to Dr. Zeinab Gura, not the whole executive list.
result = expect_contains(
    "Who is the CEO of KUTRRH?",
    "dr. zeinab gura",
    "chief executive officer"
)
print(f"Result: {result}\n")
