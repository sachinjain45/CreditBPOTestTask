from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From
import logging

logger = logging.getLogger(__name__)

def send_email(to_emails, subject, html_content, from_email=None):
    if not settings.SENDGRID_API_KEY:
        logger.warning("SENDGRID_API_KEY not set. Email not sent.")
        return False

    if not from_email:
        from_email_obj = From(settings.DEFAULT_FROM_EMAIL)
    else:
        from_email_obj = From(from_email)

    # Ensure to_emails is a list of To objects or can be converted
    if isinstance(to_emails, str):
        to_emails_list = [To(to_emails)]
    elif isinstance(to_emails, list) and all(isinstance(email, str) for email in to_emails):
        to_emails_list = [To(email) for email in to_emails]
    elif isinstance(to_emails, list) and all(isinstance(email, To) for email in to_emails):
        to_emails_list = to_emails
    else:
        logger.error(f"Invalid to_emails format: {to_emails}")
        return False

    message = Mail(
        from_email=from_email_obj,
        to_emails=to_emails_list,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {to_emails}. Subject: {subject}. Status: {response.status_code}")
        return response.status_code in [200, 201, 202] # Accepted status codes
    except Exception as e:
        logger.error(f"Error sending email to {to_emails}. Subject: {subject}. Error: {e}")
        return False

# Example email templates (very basic, use Django templates for better ones)
def send_welcome_email(user_email, user_name):
    subject = "Welcome to CreditBPO Matching Platform!"
    html_content = f"""
    <p>Hi {user_name},</p>
    <p>Welcome to the CreditBPO Matching Platform. We're excited to have you.</p>
    <p>Start exploring your dashboard: {settings.SITE_URL}/dashboard</p>
    <p>Thanks,<br/>The CreditBPO Team</p>
    """
    return send_email(user_email, subject, html_content)

def send_payment_success_email(user_email, payment_record):
    subject = f"Your Payment Was Successful - Order {payment_record.id}"
    html_content = f"""
    <p>Hi {payment_record.user.first_name or payment_record.user.username},</p>
    <p>Your payment of {payment_record.amount} {payment_record.currency} for "{payment_record.description}" was successful.</p>
    <p>Your payment ID is: {payment_record.stripe_charge_id}</p>
    <p>You can view your payment history here: {settings.SITE_URL}/dashboard/payments</p>
    <p>Thanks,<br/>The CreditBPO Team</p>
    """
    return send_email(user_email, subject, html_content)

def send_match_alert_email(seeker_email, seeker_name, provider_company_name, provider_services):
    subject = "New Potential Match Found!"
    html_content = f"""
    <p>Hi {seeker_name},</p>
    <p>We found a new potential match for your needs:</p>
    <p><strong>Provider:</strong> {provider_company_name}</p>
    <p><strong>Services:</strong> {', '.join(provider_services)}</p>
    <p>Log in to your dashboard to see more details: {settings.SITE_URL}/dashboard/matches</p>
    <p>Thanks,<br/>The CreditBPO Team</p>
    """
    return send_email(seeker_email, subject, html_content)