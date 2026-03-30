import smtplib
from email.message import EmailMessage
from pathlib import Path

import yaml
from mcp_instance import mcp

_CREDS_PATH = Path(__file__).parent.parent / ".credentials" / "mail_credentials.yaml"


def _load_credentials():
    with open(_CREDS_PATH) as f:
        return yaml.safe_load(f)


@mcp.tool()
def send_email(subject: str, body: str) -> str:
    """Send an email to the default recipient with the given subject and body.

    This tool allows the assistant to send an email on behalf of the user to a pre-configured
    recipient address. It uses SMTP to deliver the message.

    Args:
        subject: The subject line of the email to be sent.
        body: The main content/body of the email message.

    Returns:
        A string indicating the success or failure of the email sending operation.
    """
    creds = _load_credentials()
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = creds["email_user"]
    msg["To"] = creds["recipient_email"]

    try:
        # Port 587 is standard for SMTP with STARTTLS (works well for Gmail and others)
        with smtplib.SMTP(creds["smtp_host"], 587) as server:
            server.starttls()
            server.login(creds["email_user"], creds["email_password"])
            server.send_message(msg)
        return f"Successfully sent email to {creds['recipient_email']}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
