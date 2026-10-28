import httpx

from app.core.config import settings


def send_verification_email(to_email: str, token: str) -> None:
    if not settings.brevo_api_key:
        raise RuntimeError("Brevo API key is not configured.")

    if not settings.email_from:
        raise RuntimeError("Email sender is not configured.")

    message = {
        "sender": {
            "name": "DAIN",
            "email": settings.email_from,
        },
        "to": [{"email": to_email}],
        "subject": "DAIN institutional email verification",
        "textContent": f"""Welcome to DAIN.

Your verification code is:

{token}

This code expires in {settings.verification_token_ttl_minutes} minutes.

If you did not request this account, ignore this email.
""",
    }

    try:
        response = httpx.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept": "application/json",
                "api-key": settings.brevo_api_key,
                "content-type": "application/json",
            },
            json=message,
            timeout=20.0,
        )
        response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Brevo rejected the email request "
            f"(HTTP {exc.response.status_code}): "
            f"{exc.response.text[:500]}"
        ) from exc

    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Could not connect to Brevo over HTTPS."
        ) from exc
