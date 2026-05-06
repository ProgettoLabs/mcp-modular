import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown as md

from mcp_instance import mcp, load_email_credentials

@mcp.tool()
def send_email(subject: str, body: str) -> str:
    """Send an email to the default recipient with the given subject and body.

    This tool allows the assistant to send an email on behalf of the user to a pre-configured
    recipient address. It uses SMTP to deliver the message.

    Args:
        subject: The subject line of the email to be sent.
        body: The main content of the email in Markdown format. Supports headings, bold, italic,
              lists, links, code blocks, and other standard Markdown syntax. A plain-text fallback
              is generated automatically for clients that do not support HTML.

    Returns:
        A string indicating the success or failure of the email sending operation.
    """
    creds = load_email_credentials()

    html_body = md.markdown(body)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = creds["email_user"]
    msg["To"] = creds["recipient_email"]
    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        # Port 587 is standard for SMTP with STARTTLS (works well for Gmail and others)
        with smtplib.SMTP(creds["smtp_host"], 587) as server:
            server.starttls()
            server.login(creds["email_user"], creds["email_password"])
            server.send_message(msg)
        return f"Successfully sent email to {creds['recipient_email']}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
