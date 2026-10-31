"""Branch coverage tests for traffic_fine.py - Lab 6.

Goal: make every decision evaluate to BOTH True and False, with extra
focus on threshold boundaries (value just below / on / just above).
"""
import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# ============================================================ speeding_fine
# Decision 1: speed <= limit  (True -> 0, False -> keep going)
@pytest.mark.parametrize("speed, limit", [
    (50, 60),    # well below the limit
    (60, 60),    # exactly on the limit (True side of <=)
    (-5, 60),    # negative speed still counts as "not speeding"
])
def test_not_speeding_returns_zero(speed, limit):
    assert speeding_fine(speed, limit, "city") == 0


def test_one_over_the_limit_is_fined():
    # False side of <=, smallest possible excess
    assert speeding_fine(61, 60, "city") == 500


# Decisions 2 and 3: zone == "school", zone == "highway", else
@pytest.mark.parametrize("zone, expected", [
    ("school", 2000),       # first branch True
    ("highway", 1000),      # first False, second True
    ("city", 500),          # both False -> else
    ("residential", 500),   # any unknown zone -> else
    ("School", 500),        # comparison is case-sensitive -> else
    ("", 500),              # empty string -> else
])
def test_zone_selects_base_fine(zone, expected):
    assert speeding_fine(70, 60, zone) == expected   # excess 10 -> x1


# Decisions 4 and 5: excess > 40, excess > 20 (thresholds 20/21 and 40/41)
@pytest.mark.parametrize("speed, expected", [
    (80, 1000),    # excess 20 -> not > 20, multiplier x1
    (81, 2000),    # excess 21 -> > 20, x2
    (100, 2000),   # excess 40 -> not > 40, still x2
    (101, 3000),   # excess 41 -> > 40, x3
    (200, 3000),   # far above -> x3
])
def test_excess_thresholds_on_highway(speed, expected):
    assert speeding_fine(speed, 60, "highway") == expected


@pytest.mark.parametrize("zone, expected", [
    ("school", 6000),
    ("highway", 3000),
    ("city", 1500),
])
def test_top_tier_multiplier_applies_to_every_zone(zone, expected):
    assert speeding_fine(101, 60, zone) == expected   # excess 41


# ========================================================== license_action
# Decisions: points >= 12, is_commercial, points >= 8, repeat_offender,
#            points >= 4.  Each boundary is tested at (n-1) and n.
@pytest.mark.parametrize("points, commercial, repeat, expected", [
    # --- points >= 12 ---
    (12, True,  False, "revoke"),    # on threshold, commercial
    (12, False, False, "suspend"),   # on threshold, private
    (12, True,  True,  "revoke"),    # repeat flag irrelevant here
    (12, False, True,  "suspend"),
    (100, True, False, "revoke"),    # far above
    # --- 11 must NOT fall into the >= 12 block ---
    (11, True,  False, "warning"),   # commercial flag irrelevant below 12
    (11, True,  True,  "suspend"),
    # --- points >= 8 ---
    (8,  False, True,  "suspend"),   # on threshold, repeat offender
    (8,  False, False, "warning"),   # on threshold, first offence
    (7,  False, True,  "notice"),    # just below: falls to >= 4
    (7,  False, False, "notice"),
    # --- points >= 4 ---
    (4,  False, False, "notice"),    # on threshold
    (3,  False, False, "none"),      # just below
    (3,  True,  True,  "none"),      # flags irrelevant below 4
    (0,  False, False, "none"),      # minimum
])
def test_license_action_decisions(points, commercial, repeat, expected):
    assert license_action(points, commercial, repeat) == expected


# ============================================================ total_penalty
# Loop: empty (skipped) vs non-empty (iterates)
def test_empty_list_skips_loop_and_returns_zero():
    assert total_penalty([]) == 0


def test_single_fine_is_returned_unchanged():
    assert total_penalty([750]) == 750


# Decision: fine < 0
def test_zero_fine_is_allowed():
    assert total_penalty([0]) == 0


@pytest.mark.parametrize("fines", [
    [-1],                 # only fine, just below zero
    [-1, 500],            # negative first
    [500, -1, 500],       # negative in the middle
    [500, 500, -1],       # negative last
    [20000, -1],          # negative still rejected even if cap would apply
])
def test_negative_fine_raises_value_error(fines):
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty(fines)


# Decision: total > 10000  (boundary 9999 / 10000 / 10001)
@pytest.mark.parametrize("fines, expected", [
    ([9999], 9999),            # below cap
    ([5000, 5000], 10000),     # exactly on cap -> not capped, same value
    ([5000, 5001], 10000),     # 10001 -> capped
    ([10000, 1], 10000),
    ([50000], 10000),          # single huge fine
    ([4000, 4000, 4000], 10000),
])
def test_total_penalty_cap_boundaries(fines, expected):
    assert total_penalty(fines) == expected