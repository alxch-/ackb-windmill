import caldav
from datetime import datetime
from typing import Optional, Dict

from f.perso._caldav_common import (
    build_headers,
    ensure_tzaware,
    get_calendar,
    normalize_event,
)

nextcloud = dict


def main(
    NextcloudResource: nextcloud,
    userId: str,
    calendarName: str,
    uid: str,
    start: datetime,
    end: datetime,
    useAppApiAuth: bool = False,
) -> Optional[Dict[str, object]]:
    """
    Find the event with the given UID within a date range.
    """
    start = ensure_tzaware(start)
    end = ensure_tzaware(end)

    headers = build_headers(userId, NextcloudResource["password"], useAppApiAuth)

    with caldav.DAVClient(
        url=NextcloudResource["baseUrl"] + "/remote.php/dav/calendars/" + userId + "/",
        username=userId,
        password=NextcloudResource["password"],
        headers=headers,
    ) as client:
        principal = client.principal()
        calendar = get_calendar(principal, calendarName)

        raw_events = calendar.date_search(start=start, end=end)
        for ev in raw_events:
            parsed = normalize_event(ev)
            if not parsed:
                continue
            if (parsed.get("uid") or "").lower() == uid.lower():
                return parsed

        return None