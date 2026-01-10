import caldav
from datetime import datetime
from typing import Optional, Dict

from f.perso._caldav_common import build_headers, get_calendar

nextcloud = dict


def main(
    NextcloudResource: nextcloud,
    userId: str,
    calendarName: str,
    event_start: datetime,
    event_end: datetime,
    summary: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
    useAppApiAuth: bool = False,
) -> Dict[str, object]:
    """
    Create a new event with a summary, optional description and location.
    """
    headers = build_headers(userId, NextcloudResource["password"], useAppApiAuth)

    with caldav.DAVClient(
        url=NextcloudResource["baseUrl"] + "/remote.php/dav/calendars/" + userId + "/",
        username=userId,
        password=NextcloudResource["password"],
        headers=headers,
    ) as client:
        principal = client.principal()
        calendar = get_calendar(principal, calendarName)

        ev = calendar.save_event(
            dtstart=event_start,
            dtend=event_end,
            summary=summary,
            description=description,
            location=location,
        )

        return {
            "url": getattr(ev, "url", None),
            "uid": getattr(getattr(ev, "icalendar_component", None), "get", lambda *_: None)("UID"),
        }