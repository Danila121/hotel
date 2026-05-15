from django.db import models


class RequiredHotelRoomElement(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name="Название элемента",
        primary_key=True,
    )

    element_sort = models.ForeignKey(
        "RequiredElementSort",
        on_delete=models.CASCADE,
        verbose_name="Вид элемента",
    )

    room_type = models.ForeignKey(
        "HotelRoomType",
        on_delete=models.CASCADE,
        verbose_name="Тип номера",
    )

    cost = models.FloatField(
        verbose_name="Цена элемента",
    )

    class Meta:
        verbose_name = "Обязательный элемент номера"
        verbose_name_plural = "Обязательные элементы номера"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AdditionalHotelRoomElement(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name="Название элемента",
        primary_key=True,
    )

    element_sort = models.ForeignKey(
        "AdditionalElementSort",
        on_delete=models.CASCADE,
        verbose_name="Вид элемента",
    )

    room_type = models.ForeignKey(
        "HotelRoomType",
        on_delete=models.CASCADE,
        verbose_name="Тип номера",
    )

    cost = models.FloatField(
        verbose_name="Цена элемента",
    )

    class Meta:
        verbose_name = "Дополнительный элемент номера"
        verbose_name_plural = "Дополнительные элементы номера"
        ordering = ["name"]

    def __str__(self):
        return self.name


class HotelRoomType(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name="Название",
        primary_key=True,
    )

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RequiredElementSort(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name="Название",
        primary_key=True,
    )

    class Meta:
        verbose_name = "Вид обязательного элемента"
        verbose_name_plural = "Виды обязательных элементов"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AdditionalElementSort(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name="Название",
        primary_key=True,
    )

    class Meta:
        verbose_name = "Вид дополнительного элемента"
        verbose_name_plural = "Виды дополнительных элементов"
        ordering = ["name"]

    def __str__(self):
        return self.name


class IncompatibleHotelRoomElement_RequiredToRequired(models.Model):
    element1 = models.ForeignKey(
        "RequiredHotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 1",
        related_name="incompatibilities_required_as_element1",
    )

    element2 = models.ForeignKey(
        "RequiredHotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 2",
        related_name="incompatibilities_required_as_element2",
    )

    class Meta:
        verbose_name = "Несовместимые обязательные элементы номера"
        verbose_name_plural = "Несовместимые обязательные элементы номера"

        constraints = [
            models.UniqueConstraint(
                fields=["element1", "element2"],
                name="unique_incompatibility_required_required",
            ),
            models.CheckConstraint(
                condition=~models.Q(element1=models.F("element2")),
                name="prevent_self_incompatibility_required_required",
            )
        ]

    def save(self, *args, **kwargs):
        if self.element1_id > self.element2_id:
            self.element1, self.element2 = self.element2, self.element1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обязательные элементы {self.element1_id} и {self.element2_id} несовместимы"


class IncompatibleHotelRoomElement_AdditionalToAdditional(models.Model):
    element1 = models.ForeignKey(
        "AdditionalHotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 1",
        related_name="incompatibilities_additional_as_element1",
    )

    element2 = models.ForeignKey(
        "AdditionalHotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 2",
        related_name="incompatibilities_additional_as_element2",
    )

    class Meta:
        verbose_name = "Несовместимые дополнительные элементы номера"
        verbose_name_plural = "Несовместимые дополнительные элементы номера"

        constraints = [
            models.UniqueConstraint(
                fields=["element1", "element2"],
                name="unique_incompatibility_additional_additional",
            ),
            models.CheckConstraint(
                condition=~models.Q(element1=models.F("element2")),
                name="prevent_self_incompatibility_additional_additional",
            )
        ]

    def save(self, *args, **kwargs):
        if self.element1_id > self.element2_id:
            self.element1, self.element2 = self.element2, self.element1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Дополнительные элементы {self.element1_id} и {self.element2_id} несовместимы"


class IncompatibleHotelRoomElement_RequiredToAdditional(models.Model):
    element1 = models.ForeignKey(
        "RequiredHotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 1",
        related_name="incompatibilities_required_to_additional_as_element1",
    )

    element2 = models.ForeignKey(
        "AdditionalHotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 2",
        related_name="incompatibilities_required_to_additional_as_element2",
    )

    class Meta:
        verbose_name = "Несовместимые обязательные и дополнительные элементы номера"
        verbose_name_plural = "Несовместимые обязательные и дополнительные элементы номера"

        constraints = [
            models.UniqueConstraint(
                fields=["element1", "element2"],
                name="unique_incompatibility_required_additional",
            ),
            models.CheckConstraint(
                condition=~models.Q(element1=models.F("element2")),
                name="prevent_self_incompatibility_required_additional",
            )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обязательный элемент {self.element1_id} и дополнительный элемент {self.element2_id} несовместимы"