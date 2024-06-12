from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Override Django's PasswordResetTokenGenerator to generate tokens for email verification
    """
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.email_is_verified)
        )


account_activation_token = TokenGenerator()  # Generate new token for the current user
