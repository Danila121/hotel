from django.db import models


class RoomElement(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )

    name = models.CharField(
        max_length=500,
        verbose_name="Название элемента",
    )

    min_price_category = models.ForeignKey(
        "PriceCategory",
        on_delete=models.CASCADE,
        verbose_name="Ценовая категория",
    )

    room_id = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        verbose_name="Идентификатор",
    )

    is_required = models.BooleanField(
        default=True,
        verbose_name="Обязательный элемент",
    )

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
        ordering = ["id"]


class Room(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )

    price_category = models.ForeignKey(
        "PriceCategory",
        on_delete=models.CASCADE,
        verbose_name="Ценовая категория",
    )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        ordering = ["id"]


class PriceCategory(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )

    name = models.CharField(
        max_length=500,
        verbose_name="Название",
    )

    class Meta:
        verbose_name = "Ценовая категория"
        verbose_name_plural = "Ценовые категории"
        ordering = ["id"]


class IncompatibleRoomElement(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )

    element_id = models.ForeignKey(
        "RoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 1",
        related_name="incompatibilities_as_element1",
    )

    incompatible_element_id = models.ForeignKey(
        "RoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 2",
        related_name="incompatibilities_as_element2",
    )

    class Meta:
        verbose_name = "Несовместимые элементы"
        verbose_name_plural = "Несовместимые элементы"
        ordering = ["id"]
