from django.db import models

class PetroleumData(models.Model):
    year = models.CharField(max_length=4)
    petroleum_product = models.CharField(max_length=255)
    sale = models.IntegerField()
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.year} - {self.petroleum_product} ({self.country})"
