from django.db import models
from django.utils.safestring import SafeText


class Device(models.Model):
    imei = models.CharField(max_length=32)

    def __str__(self):
        return self.imei

    @property
    def last_position(self):
        return self.positions.order_by('-datetime').first()

    @property
    def last_position_view_link(self):
        pos = self.positions.order_by('-datetime').first()
        if pos:
            return pos.view_link
        return None

    @property
    def last_position_datetime(self):
        pos = self.positions.order_by('-datetime').first()
        if pos:
            return pos.datetime
        return None


class Position(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='positions')
    latitude = models.FloatField()
    longitude = models.FloatField()
    datetime = models.DateTimeField()

    class Meta:
        ordering = ('-datetime',)

    def __str__(self):
        return f'{self.latitude},{self.longitude}'

    @property
    def view_link(self):
        url = f'https://www.openstreetmap.org/#map=19/{self.latitude}/{self.longitude}'
        return SafeText(f'<a target="_blank" href="{url}">OpenStreetMap</a>')

    @property
    def position(self):
        return f'{self.latitude},{self.longitude}'
