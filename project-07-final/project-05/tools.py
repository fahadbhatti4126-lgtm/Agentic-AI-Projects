from langchain_core.tools import tool


@tool
def prepare_email(recipient: str, subject: str, message: str) -> str:
    """
    Prepare an email message.
    This tool does not send the email.
    """

    return f"""
EMAIL PREPARED

To: {recipient}
Subject: {subject}

Message:
{message}
"""


@tool
def prepare_notification(title: str, message: str) -> str:
    """
    Prepare a notification message.
    This tool does not send the notification.
    """

    return f"""
NOTIFICATION PREPARED

Title: {title}

Message:
{message}
"""