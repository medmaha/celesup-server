from django.db import models

class UniqueId(models.Model):
    used_for = models.CharField(max_length=100, null=True, blank=True)
    unique_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}. {self.used_for} -- {self.unique_id}'

    class Meta:
        verbose_name_plural = "UniqueId's"



