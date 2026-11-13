import re

MAX_FINE = 10000
_DIGITS = re.compile(r"[0-9]{1,9}")  # ASCII digits only, bounded length


def _to_int(text):
    """Return int for a string of 1-9 ASCII digits (after strip), else None."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    return int(text) if _DIGITS.fullmatch(text) else None


def parse_ticket_id(ticket_id):
    """Parse 'PREFIX-YEAR-SERIAL'. Returns (PREFIX, year, serial) or None if invalid."""
    if not isinstance(ticket_id, str):
        return None
    parts = ticket_id.strip().split('-')
    if len(parts) != 3:
        return None
    prefix, year, serial = (p.strip() for p in parts)
    if not (prefix.isascii() and prefix.isalpha()):
        return None
    year, serial = _to_int(year), _to_int(serial)
    if year is None or serial is None:
        return None
    return prefix.upper(), year, serial


def total_fines(amounts_csv):
    """Sum comma separated fines, capped at MAX_FINE. Returns None if invalid."""
    if not isinstance(amounts_csv, str):
        return None
    amounts = [_to_int(a) for a in amounts_csv.split(',')]
    if not amounts or any(a is None for a in amounts):
        return None
    return min(sum(amounts), MAX_FINE)


def speed_excess(reading):
    """Percent over limit for 'speed/limit'. Returns None if invalid or limit is 0."""
    if not isinstance(reading, str):
        return None
    parts = reading.split('/')
    if len(parts) != 2:
        return None
    speed, limit = _to_int(parts[0]), _to_int(parts[1])
    if speed is None or limit is None or limit == 0:
        return None
    return (speed - limit) * 100 // limit


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    print("Ticket Prefix, Year and Serial:", result if result else "Invalid ticket ID")

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    print("Total Fines:", result if result is not None else "Invalid fine amounts")

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    print("Percent Over Limit:", result if result is not None else "Invalid reading")


if __name__ == "__main__":
    main()
