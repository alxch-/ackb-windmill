#requirements:
#imap-tools

from imap_tools import MailBox, AND


def main(
    imap_resource: dict,
    folder: str,
    excluded_senders: list[str],
) -> list[dict]:
    """
    Fetch new unread emails.

    Args:
        imap_resource: {host, user, password}
        folder: Mailbox folder
    """
    emails = []

    with MailBox(imap_resource["host"]).login(
        imap_resource["user"],
        imap_resource["password"],
        folder
    ) as mailbox:
        for msg in mailbox.fetch(AND(seen=False), mark_seen=True):
            # Skip excluded senders
            if any(ex in msg.from_.lower() for ex in excluded_senders):
                continue
            emails.append({
                "subject": msg.subject,
                "sender": msg.from_,
                "html_body": msg.html or msg.text,
                "date": msg.date.isoformat() if msg.date else None
            })
    return emails