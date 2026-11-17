from storage import (
    load_events,
    load_registrations,
    save_events,
    save_registrations,
)


def test_events_roundtrip(tmp_path):
    filename = str(tmp_path / "events.json")
    events = {1: {"title": "Семинар", "date": "2026-12-03", "capacity": 30}}
    save_events(filename, events)
    assert load_events(filename) == events


def test_registrations_roundtrip(tmp_path):
    filename = str(tmp_path / "registrations.json")
    items = [{"id": 1, "event_id": 1, "employee": "Иван Петров"}]
    save_registrations(filename, items)
    assert load_registrations(filename) == items


def test_missing_and_broken_file(tmp_path):
    assert load_events(str(tmp_path / "none.json")) == {}
    broken = tmp_path / "broken.json"
    broken.write_text("{не json", encoding="utf-8")
    assert load_registrations(str(broken)) == []
