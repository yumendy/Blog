from __future__ import unicode_literals

from django.db import models
from Blog.local_settings import storage

MOOD_TYPE_CHOICE = (
    ('T', 'Text'),
    ('I', 'Image'),
    ('B', 'block_quote')
)


class Mood(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    mood_type = models.CharField(max_length=1, choices=MOOD_TYPE_CHOICE, default='T')
    image = models.ImageField(upload_to='./image/mood/%Y/%m/%d/', null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    def get_small_image_url(self):
        if storage == 'qiniu':
            return self.image.url + '?imageView2/2/w/350'
        else:
            return self.image.url

    class Meta:
        ordering = ['-create_time']

