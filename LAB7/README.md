# LAB 7 - Fuzzing for Input Validation Bugs (Traffic Fine Calculator)

| File | Description |
|------|-------------|
| `buggy/traffic_fine.py` | Original instructor code (unchanged, kept as evidence) |
| `traffic_fine.py` | Fixed / hardened script |
| `test_traffic_fine.py` | Hypothesis fuzz + property tests |
| `Lab7_Fuzzing_Report.pdf` | Output screenshots (Steps 2, 4, 5, 6) |

## Bugs found
| Function | Crash input | Cause |
|---|---|---|
| `parse_ticket_id` | `""`, `"TF-2024"`, `None` | tuple unpack of wrong number of parts, non-numeric `int()`, `.split` on None |
| `total_fines` | `""`, `"1,,3"`, `"a,b"`, `None` | `int('')` ValueError, None has no `.split`; negatives not rejected |
| `speed_excess` | `"72/0"`, `"abc"`, `None` | ZeroDivisionError, bad unpack, None |

## Fix
Type check, strict ASCII-digit validation, exact part counts, zero-limit guard. Invalid input returns `None` instead of raising.

Run: `python traffic_fine.py` and `python -m pytest test_traffic_fine.py`
