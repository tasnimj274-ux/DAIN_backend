"""Replaceable institutional-verification boundary for the DAIN MVP."""

from app.core.config import settings


class InstitutionalEmailVerificationPrototype:
    """Validate university email domains, including department subdomains."""

    def accepts(self, email: str) -> bool:
        domain = email.rsplit("@", 1)[-1].strip().lower()
        institutional_domain = (
            settings.institutional_email_domain.strip().lower()
        )

        return (
            domain == institutional_domain
            or domain.endswith(f".{institutional_domain}")
        )


institutional_verifier = InstitutionalEmailVerificationPrototype()

