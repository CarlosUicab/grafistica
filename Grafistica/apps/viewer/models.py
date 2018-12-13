from django.db import models
import os
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    def image_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "Users/id-%s/profile/%s.%s" % (self.user.id, slugify(str(file_name)), extension)
        return url

    user = models.OneToOneField(User)
    image = models.ImageField(upload_to=image_path, null=True, blank=True, verbose_name=_("Foto de perfil"))

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("Perfil de usuario")
        verbose_name_plural = _("Perfil de usuarios")


class FileTemp(models.Model):

    def file_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "tmp/%s.%s" % (slugify(str(file_name)), extension)
        return url

    file = models.FileField(upload_to=file_path)


class ExcelData(models.Model):
    username = models.ForeignKey(User)
    excel_name = models.CharField(max_length=500)
    # excel_sheet = models.CharField(max_length=500)
    data = JSONField()


class GraphExcelData(models.Model):
    username = models.ForeignKey(User)
    excel_name = models.CharField(max_length=500)
    graph_key = models.IntegerField(default=1)


class DataAnalytic(models.Model):

    def file_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "tmp/%s.%s" % (slugify(str(file_name)), extension)
        return url

    user = models.ForeignKey(User)
    file = models.FileField(upload_to=file_path)
    name = models.CharField(null=True, blank=True, max_length=10000)
    json = JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else str(self.timestamp)

    def save(self, *args, **kwargs):
        if self.file and not self.id:
            self.name = self.file.name
        super(DataAnalytic, self).save(*args, **kwargs)


class Chart(models.Model):

    __charts = (
        (1, 'Line chart'),
        (2, 'Bar chart'),
        (3, 'Column chart'),
        (4, 'Pie chart'),
        (5, 'Spline chart'),
        (6, 'Basic Area Chart'),
        (7, 'Area Spline chart'),
        (8, 'Waterfall chart'),
        (9, 'Polygon chart'),
        (10, 'Scatter Chart')
    )

    type_key = models.PositiveIntegerField(_('Tipo'), choices=__charts)
    # name = models.CharField(verbose_name=_('Nombre'), max_length=50)
    position_x = models.CharField(verbose_name=_('Posición X'), max_length=100, null=True, blank=True)
    position_y = models.CharField(verbose_name=_('Posición Y'), max_length=100, null=True, blank=True)
    label = models.CharField(verbose_name=_('Posición'), max_length=100, null=True, blank=True)
    data_file = models.ForeignKey(DataAnalytic)
    #
    # def __str__(self):
    #     return self.

