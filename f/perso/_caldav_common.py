import base64
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import caldav
from icalendar import Calendar as ICalCalendar

nextcloud = dict


def build_headers(user_id: str, password: str, use_app_api_auth: bool) -> Dict[str, str]:
    if not use_app_api_auth:
        return {}
    return {
        "AA-VERSION": "2.3.0",
        "EX-APP-ID": "flow",
        "EX-APP-VERSION": "1.0.0",
        "AUTHORIZATION-APP-API": base64.b64encode(
            f"{user_id}:{password}".encode("utf-8")
        ).decode("utf-8"),
    }


def ensure_tzaware(dt: datetime, fallback_tz=timezone.utc) -> datetime:
    """
    Make sure a datetime is timezone aware.
    Windmill sometimes gives naive datetimes.
    """
    if dt is None:
        return dt
    if getattr(dt, "tzinfo", None) is None:
        return dt.replace(tzinfo=fallback_tz)
    return dt


def get_calendar(principal, calendar_name: str):
    """
    Find a calendar by name on the principal.
    """
    cal = next((c for c in principal.calendars() if c.name == calendar_name), None)
    if cal is None:
        raise ValueError(f"Calendar '{calendar_name}' not found")
    return cal


def _to_list(v) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]


def parse_first_vevent(ics_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse only the first VEVENT in an iCal string.
    """
    cal = ICalCalendar.from_ical(ics_text)
    vevent = None
    for comp in cal.walk():
        if comp.name == "VEVENT":
            vevent = comp
            break
    if vevent is None:
        return None

    def decoded(prop):
        if prop is None:
            return None
        try:
            return prop.dt
        except Exception:
            return str(prop)

    dtstart = vevent.get("DTSTART")
    dtend = vevent.get("DTEND")

    return {
        "uid": str(vevent.get("UID")) if vevent.get("UID") is not None else None,
        "summary": str(vevent.get("SUMMARY")) if vevent.get("SUMMARY") is not None else None,
        "description": str(vevent.get("DESCRIPTION")) if vevent.get("DESCRIPTION") is not None else None,
        "location": str(vevent.get("LOCATION")) if vevent.get("LOCATION") is not None else None,
        "dtstart": decoded(dtstart),
        "dtend": decoded(dtend),
        "status": str(vevent.get("STATUS")) if vevent.get("STATUS") is not None else None,
        "transparency": str(vevent.get("TRANSP")) if vevent.get("TRANSP") is not None else None,
        "categories": _to_list(vevent.get("CATEGORIES")),
        "organizer": str(vevent.get("ORGANIZER")) if vevent.get("ORGANIZER") is not None else None,
        "attendees": _to_list(vevent.get("ATTENDEE")),
    }


def normalize_event(ev) -> Optional[Dict[str, Any]]:
    """
    Convert a caldav event to a simple dict.
    """
    try:
        ics = ev.data
        if isinstance(ics, (bytes, bytearray)):
            ics = ics.decode("utf-8", errors="replace")
        parsed = parse_first_vevent(ics)
        if not parsed:
            return None
        parsed["ics"] = ics
        return parsed
    except Exception:
        return None


def matches_q(parsed: Dict[str, Any], q: str) -> bool:
    """
    A basic text search across common event fields.
    """
    if not q:
        return True
    ql = q.lower()
    hay = " ".join(
        [
            parsed.get("summary") or "",
            parsed.get("description") or "",
            parsed.get("location") or "",
            parsed.get("uid") or "",
            " ".join(parsed.get("categories") or []),
            parsed.get("organizer") or "",
            " ".join(parsed.get("attendees") or []),
        ]
    ).lower()
    return ql in hay