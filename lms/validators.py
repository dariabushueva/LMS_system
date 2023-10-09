import re

from rest_framework.exceptions import ValidationError


class VideoUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value is None or value.get(self.field, '').strip() == '':
            return
        youtube_url = re.compile("(https?://)?(www\.)?(youtube\.com|youtu\.be)/watch\?v=([A-Za-z0-9_-]+)")
        tmp_value = dict(value).get(self.field)
        if not bool(youtube_url.match(tmp_value)):
            raise ValidationError('Ссылка может быть только на YouTube')


