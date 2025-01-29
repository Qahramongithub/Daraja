from django.db import models


class Category(models.Model):
    nomi = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Yarm Tayor Kategoriyasi'

    def __str__(self):
        return self.nomi


class Product(models.Model):
    soni = models.IntegerField()
    nomi = models.ForeignKey('apps.Category', on_delete=models.CASCADE, null=True, blank=True,
                             related_name='products')

    class Meta:
        verbose_name_plural = "Yarm Tayor Maxsulotlar"

    def __str__(self):
        return self.nomi.nomi


class FinishCategory(models.Model):
    nomi = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Tayor maxsulotlar Kategoriasi'

    def __str__(self):
        return self.nomi


class FinishProduct(models.Model):
    soni = models.IntegerField()
    nomi = models.ForeignKey('apps.FinishCategory', on_delete=models.CASCADE, null=True, blank=True, )

    class Meta:
        verbose_name_plural = 'Tayor maxsulotlar'

    def __str__(self):
        return self.nomi


class ProductHistory(models.Model):
    class StatusType(models.TextChoices):
        CHIQDI = 'chiqdi', 'Chiqdi'
        QABUL = 'qabul', 'Qabul'

    nomi = models.ForeignKey('apps.Category', on_delete=models.CASCADE, null=True, blank=True, )
    soni = models.IntegerField()
    status = models.CharField(choices=StatusType.choices, default=StatusType.CHIQDI, max_length=100)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Yarm Tayor maxsulotlar'


class FinishProductHistory(models.Model):
    class StatusType(models.TextChoices):
        CHIQDI = 'chiqdi', 'Chiqdi'
        QABUL = 'qabul', 'Qabul'

    nomi = models.ForeignKey('apps.FinishCategory', on_delete=models.CASCADE, null=True, blank=True, )
    soni = models.IntegerField()
    status = models.CharField(choices=StatusType.choices, default=StatusType.CHIQDI, max_length=100)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Tayor maxsulotlar'
