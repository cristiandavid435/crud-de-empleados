from django.contrib.auth.password_validation import CommonPasswordValidator, get_default_password_validators
from django.core.exceptions import ValidationError


class NumericPasswordValidator:
    """Validador para asegurar que la contraseña no sea completamente numérica."""

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "La contraseña no puede estar compuesta enteramente por números.",
                code='numeric_password',
            )

    def get_help_text(self):
        return "La contraseña no puede estar compuesta enteramente por números."
