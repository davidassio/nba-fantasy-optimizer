SALARY_CAP = 50000

ROSTER_SLOTS = [
    "PG",
    "SG",
    "SF",
    "PF",
    "C",
    "G",
    "F",
    "UTIL",
]

SLOT_ELIGIBILITY = {
    "PG": {"PG"},
    "SG": {"SG"},
    "SF": {"SF"},
    "PF": {"PF"},
    "C": {"C"},
    "G": {"PG", "SG"},
    "F": {"SF", "PF"},
    "UTIL": {"PG", "SG", "SF", "PF", "C"},
}