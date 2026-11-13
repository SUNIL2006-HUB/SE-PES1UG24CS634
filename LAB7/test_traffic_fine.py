from hypothesis import given, strategies as st
from traffic_fine import parse_ticket_id, total_fines, speed_excess


# ---------- 1. No-crash (fuzz) tests: any input must not raise ----------

@given(st.text() | st.none())
def test_parse_ticket_id_no_crash(s):
    try:
        parse_ticket_id(s)
    except Exception as e:
        assert False, f"parse_ticket_id crashed with: {e!r}"


@given(st.text() | st.none())
def test_total_fines_no_crash(s):
    try:
        total_fines(s)
    except Exception as e:
        assert False, f"total_fines crashed with: {e!r}"


@given(st.text() | st.none())
def test_speed_excess_no_crash(s):
    try:
        speed_excess(s)
    except Exception as e:
        assert False, f"speed_excess crashed with: {e!r}"


# ---------- 2. Property tests: valid input gives correct output ----------

@given(st.from_regex(r"[A-Za-z]{1,5}", fullmatch=True),
       st.integers(1000, 9999), st.integers(0, 10**6))
def test_parse_ticket_id_valid(prefix, year, serial):
    ticket = f"{prefix}-{year}-{serial}"
    assert parse_ticket_id(ticket) == (prefix.upper(), year, serial)


@given(st.lists(st.integers(0, 5000), min_size=1, max_size=20))
def test_total_fines_valid_capped(amounts):
    result = total_fines(",".join(map(str, amounts)))
    assert result == min(sum(amounts), 10000)
    assert 0 <= result <= 10000


@given(st.integers(0, 400), st.integers(1, 200))
def test_speed_excess_valid(speed, limit):
    assert speed_excess(f"{speed}/{limit}") == (speed - limit) * 100 // limit


# ---------- 3. Explicit edge cases found by fuzzing ----------

def test_known_edge_cases():
    assert parse_ticket_id("TF-2024-0456") == ("TF", 2024, 456)
    assert parse_ticket_id("") is None
    assert parse_ticket_id("TF-2024") is None
    assert parse_ticket_id("TF-2024-1-2") is None
    assert parse_ticket_id(None) is None
    assert total_fines("500,1200,300") == 2000
    assert total_fines("") is None
    assert total_fines("1,,3") is None
    assert total_fines("5000,6000") == 10000
    assert total_fines(None) is None
    assert speed_excess("72/60") == 20
    assert speed_excess("72/0") is None
    assert speed_excess("abc") is None
    assert speed_excess(None) is None
