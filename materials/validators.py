from rest_framework.serializers import ValidationError


class ValidateUrlVideo:
    """
    Проверка URL-адреса видео.
    Должно быть с youtube.com
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        valv = dict(value).get(self.field)
        if 'youtube.com' not in valv:
            raise ValidationError('URL-адрес должен быть с YouTube')
