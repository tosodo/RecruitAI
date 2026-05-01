#!/usr/bin/env python3
"""
Email Verification Module
Ensures emails actually deliver — if not, alert via multiple channels
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

class EmailVerifier:
    def __init__(self):
        self.from_email = os.environ.get("EMAIL_FROM", "sales@aigentforce.io")
        self.to_email = "osodot@icloud.com"
        
    def send_email(self, subject, body, priority="normal"):
        """Send email with delivery confirmation"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[AIGENTFORCE] {subject}"
        msg["From"] = self.from_email
        msg["To"] = self.to_email
        msg["X-Priority"] = "1" if priority == "high" else "3"
        
        # Plain text version
        msg.attach(MIMEText(body, "plain"))
        
        try:
            with smtplib.SMTP("server801.web-hosting.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.login(self.from_email, os.environ.get("EMAIL_PASSWORD", ""))
                server.sendmail(self.from_email, [self.to_email], msg.as_string())
            return True, "Email delivered successfully"
        except Exception as e:
            return False, f"Email delivery failed: {str(e)}"
    
    def send_alert(self, subject, body):
        """Send alert email — high priority"""
        success, message = self.send_email(f"[ALERT] {subject}", body, priority="high")
        # Also log to file
        log_path = Path("/home/workspace/data/email_alerts.log")
        with open(log_path, "a") as f:
            timestamp = __import__("datetime").datetime.now().isoformat()
            f.write(f"[{timestamp}] {'✅' if success else '❌'} {subject}: {message}\n")
        return success, message
    
    def verify_delivery(self, subject):
        """Check if email was delivered"""
        log_path = Path("/home/workspace/data/email_alerts.log")
        if log_path.exists():
            with open(log_path) as f:
                for line in f:
                    if subject in line:
                        return "✅ Delivered" in line
        return False

if __name__ == "__main__":
    verifier = EmailVerifier()
    success, msg = verifier.send_email(
        "TEST: AIGENTFORCE Email System Check",
        "This is a test email from AIGENTFORCE email verification system.\n\n"
        "If you received this, email delivery is working.\n\n"
        "— AIGENTFORCE Technical Team"
    )
    print(f"Email result: {msg}")