import smtplib
from email.message import EmailMessage
import os
from ..core.config import settings
from .otp import generate_otp

def send_otp_email(to_email: str, otp: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Your One-Time Password (OTP)"
        msg["From"] = settings.from_email
        msg["To"] = to_email
        msg.set_content(
            f"""Hello,

        Your One-Time Password (OTP) is:

        {otp}

        This code is valid for a limited time. Please do not share it with anyone.

        If you did not request this code, you can safely ignore this email.

        Best regards,
        The GiveHub Team
        """
        )

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_pass)
            server.send_message(msg)

        print("✅ OTP email sent")

    except Exception as e:
        print("❌ Email failed:", e)
        raise

def send_payment_done_email(to_email: str, amount: int):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Thank You for Your Donation"
        msg["From"] = settings.from_email
        msg["To"] = to_email
        msg.set_content(
            f"""Hello,

        Thank you for your generosity! We have successfully received your donation of ${amount}.

        Your support helps us continue our mission and make a meaningful impact.

        If you have any questions or did not make this donation, please contact our support team.

        With gratitude,
        The GiveHub Team
        """
        )


        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_pass)
            server.send_message(msg)
        
        print("✅ Acknowledgement email sent")
    except Exception as e:
        print("❌ Acknowledgement email failed", e)
        raise
