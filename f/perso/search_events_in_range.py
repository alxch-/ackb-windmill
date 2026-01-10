import caldav
from datetime import datetime
from typing import Optional, Dict

from f.perso._caldav_common import (
    build_headers,
    ensure_tzaware,
    get_calendar,
    normalize_event,
    matches_q,
)

nextcloud = dict


def main(
    NextcloudResource: nextcloud,
    userId: str,
    calendarName: str,
    start: datetime,
    end: datetime,
    q: Optional[str] = None,
    limit: int = 50,
    useAppApiAuth: bool = False,
) -> Dict[str, object]:
    """
    Search events in a calendar between start and end.
    Optionally match a query string `q`.
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

        items = []
        for ev in raw_events:
            parsed = normalize_event(ev)
            if not parsed:
                continue
            if not matches_q(parsed, q):
                continue
            items.append(parsed)
            if len(items) >= limit:
                break

        return {"count": len(items), "items": items}