"""Code (line) coverage tests for traffic_fine.py - Lab 6.

Goal: execute every line of speeding_fine, license_action and
total_penalty at least once, and check the returned values.
"""
import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# ---------------------------------------------------------------- speeding_fine
def test_no_speeding():
    # Starter test: below the limit -> no fine
    assert speeding_fine(50, 60, "city") == 0


def test_speed_equal_to_limit_is_not_fined():
    assert speeding_fine(60, 60, "highway") == 0


def test_school_zone_moderate_excess_doubles_base():
    # excess = 30 (> 20, <= 40): school base 2000 * 2
    assert speeding_fine(90, 60, "school") == 4000


def test_highway_small_excess_returns_base():
    # excess = 5 (<= 20): highway base 1000
    assert speeding_fine(85, 80, "highway") == 1000


def test_other_zone_large_excess_triples_base():
    # excess = 60 (> 40): default base 500 * 3
    assert speeding_fine(120, 60, "city") == 1500


# -------------------------------------------------------------- license_action
def test_clean_record():
    # Starter test: fewer than 4 points
    assert license_action(2, False, False) == "none"


def test_twelve_points_commercial_is_revoked():
    assert license_action(12, True, False) == "revoke"


def test_twelve_points_private_driver_is_suspended():
    assert license_action(15, False, False) == "suspend"


def test_eight_points_repeat_offender_is_suspended():
    assert license_action(8, False, True) == "suspend"


def test_eight_points_first_offence_gets_warning():
    assert license_action(9, False, False) == "warning"


def test_four_points_gets_notice():
    assert license_action(5, False, False) == "notice"


# -------------------------------------------------------------- total_penalty
def test_total_penalty_sums_fines():
    assert total_penalty([500, 1000, 250]) == 1750


def test_total_penalty_negative_fine_raises_value_error():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([500, -1])


def test_total_penalty_is_capped_at_10000():
    assert total_penalty([6000, 7000]) == 10000