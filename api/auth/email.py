"""Email adapter — Resend.

Sadece 2 email tipi gönderir:
  1. Email verification (register sonrası)
  2. Password reset (forgot-password sonrası)

Fail-safe: email fail olursa exception RAISE ETMEZ, log atar. Kullanıcı akışı
kesilmez — kullanıcı email gelmediyse "yeniden yolla" butonu ile tetikler.
"""
import logging
import os
from typing import Optional

import resend

log = logging.getLogger(__name__)

_API_KEY = os.environ.get("CBT_RESEND_API_KEY")
_FROM = os.environ.get("CBT_EMAIL_FROM", "onboarding@resend.dev")
_APP_URL = os.environ.get("CBT_APP_URL", "http://localhost:3000")

if _API_KEY:
    resend.api_key = _API_KEY
else:
    log.warning("CBT_RESEND_API_KEY not set — emails will not be sent")

def send_verification_email(email: str, token: str) -> bool:
    """Verify email link. Returns True on success."""
    if not _API_KEY:
        log.warning(f"[skip email] verification link for {email}: {_APP_URL}/auth/verify?token={token}")
        return False

    verify_url = f"{_APP_URL}/auth/verify?token={token}"
    html = _verification_html(verify_url)

    try:
        resend.Emails.send({
            "from": _FROM,
            "to": [email],
            "subject": "E-posta adresini doğrula",
            "html": html,
        })
        return True
    except Exception as e:
        log.warning(f"send_verification_email failed for {email}: {e}")
        return False
    
def send_password_reset_email(email: str, token: str) -> bool:
    """Password reset link. Returns True on success."""
    if not _API_KEY:
        log.warning(f"[skip email] reset link for {email}: {_APP_URL}/auth/reset?token={token}")
        return False

    reset_url = f"{_APP_URL}/auth/reset?token={token}"
    html = _reset_html(reset_url)

    try:
        resend.Emails.send({
            "from": _FROM,
            "to": [email],
            "subject": "Şifreni sıfırla",
            "html": html,
        })
        return True
    except Exception as e:
        log.warning(f"send_password_reset_email failed for {email}: {e}")
        return False

def _verification_html(verify_url: str) -> str:
    return f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; color: #1f2937;">
      <h2 style="font-weight: 500; color: #0f172a;">E-postanı doğrula</h2>
      <p style="line-height: 1.6;">
        CBT Destek hesabını oluşturduğun için teşekkürler.
        Devam etmek için lütfen e-posta adresini doğrula:
      </p>
      <p style="margin: 30px 0;">
        <a href="{verify_url}" style="background: #0ea5e9; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: inline-block;">
          E-postamı doğrula
        </a>
      </p>
      <p style="color: #6b7280; font-size: 13px; line-height: 1.5;">
        Bu link 24 saat geçerli. Hesap oluşturmadıysan bu e-postayı yok say.
        <br><br>
        Link tıklanmıyorsa şu adresi tarayıcına kopyala:<br>
        <span style="word-break: break-all;">{verify_url}</span>
      </p>
    </div>
    """

def _reset_html(reset_url: str) -> str:
    return f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; color: #1f2937;">
      <h2 style="font-weight: 500; color: #0f172a;">Şifre sıfırlama</h2>
      <p style="line-height: 1.6;">
        Hesabın için şifre sıfırlama talebi aldık. Yeni şifreni belirlemek için:
      </p>
      <p style="margin: 30px 0;">
        <a href="{reset_url}" style="background: #0ea5e9; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: inline-block;">
          Şifremi sıfırla
        </a>
      </p>
      <p style="color: #6b7280; font-size: 13px; line-height: 1.5;">
        Bu link 1 saat geçerli. Şifre sıfırlama talebinde bulunmadıysan bu
        e-postayı yok say — mevcut şifren değişmez.
      </p>
    </div>
    """

