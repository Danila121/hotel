from django.db import models


class HotelRoomElement(models.Model):

    name = models.CharField(
        max_length=500,
        verbose_name="Название элемента",
        primary_key=True,
    )

    element_sort = models.ForeignKey(
        "ElementSort",
        on_delete=models.CASCADE,
        verbose_name="Вид элемента",
    )

    room_type = models.ForeignKey(
        "HotelRoomType",
        on_delete=models.CASCADE,
        verbose_name="Тип номера",
    )

    class Meta:
        verbose_name = "Элемент номера"
        verbose_name_plural = "Элементы номеров"
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


class ElementSort(models.Model):

    name = models.CharField(
        max_length=500,
        verbose_name="Название",
        primary_key=True,
    )

    is_required = models.BooleanField(
        default=False,
        verbose_name="Обязательный элемент",
    )

    class Meta:
        verbose_name = "Вид элемента"
        verbose_name_plural = "Виды элементов"
        ordering = ["name"]

    def __str__(self):
        return self.name


class IncompatibleRoomElement(models.Model):

    element = models.ForeignKey(
        "HotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 1",
        related_name="incompatibilities_as_element1",
    )

    incompatible_element = models.ForeignKey(
        "HotelRoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 2",
        related_name="incompatibilities_as_element2",
    )

    class Meta:
        verbose_name = "Несовместимые элементы номеров"
        verbose_name_plural = "Несовместимые элементы номеров"

        constraints = [

            models.UniqueConstraint(
                fields=["element", "incompatible_element"],
                name="unique_incompatibility",
            ),

        models.CheckConstraint(
            condition=~models.Q(
                element=models.F("incompatible_element")
            ),
            name="prevent_self_incompatibility",
        )

        ]

    def save(self, *args, **kwargs):
        if self.element_id > self.incompatible_element_id:
            self.element, self.incompatible_element = (
                self.incompatible_element,
                self.element,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Элементы {self.element_id} и {self.incompatible_element_id} несовместимы"
        )
