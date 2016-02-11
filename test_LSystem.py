from LSystem import LSystem, LSystemOverflow
from nose.tools import raises

ALGAE_START = "A"
ALGAE_RULES = {
    "A": "AB",
    "B": "A"
}
ALGAE_RESULTS = ["A", "AB", "ABA", "ABAAB", "ABAABABA", "ABAABABAABAAB"]

def test_results():

    def trial(system, n, result):
        assert system.nth(n) == result

    system = LSystem(ALGAE_START, ALGAE_RULES)
    for i, result in enumerate(ALGAE_RESULTS):
        yield trial, system, i, result

@raises(LSystemOverflow)
def test_overflow():
    system = LSystem(ALGAE_START, ALGAE_RULES, 10)
    system.nth(10)
