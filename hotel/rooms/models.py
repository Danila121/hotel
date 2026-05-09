from django.db import models


class RoomElement(models.Model):

    name = models.CharField(
        max_length=500,
        verbose_name="Название элемента",
    )

    element_type = models.ForeignKey(
        "ElementType",
        on_delete=models.CASCADE,
        verbose_name="Тип элемента",
    )

    room_type = models.ForeignKey(
        "RoomType",
        on_delete=models.CASCADE,
        verbose_name="Подходящий тип комнаты",
    )

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Room(models.Model):

    room_type = models.ForeignKey(
        "RoomType",
        on_delete=models.CASCADE,
        verbose_name="Тип комнаты",
    )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        ordering = ["id"]

    def __str__(self):
        return f"Комната {self.id}"


class RoomType(models.Model):

    name = models.CharField(
        max_length=500,
        verbose_name="Название",
    )

    class Meta:
        verbose_name = "Тип комнаты"
        verbose_name_plural = "Типы комнат"
        ordering = ["id"]

    def __str__(self):
        return self.name


class ElementType(models.Model):

    name = models.CharField(
        max_length=500,
        verbose_name="Название",
    )

    is_required = models.BooleanField(
        default=False,
        verbose_name="Обязательный элемент",
    )

    class Meta:
        verbose_name = "Тип элемента"
        verbose_name_plural = "Типы элементов"
        ordering = ["id"]

    def __str__(self):
        return self.name


class IncompatibleRoomElement(models.Model):

    element = models.ForeignKey(
        "RoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 1",
        related_name="incompatibilities_as_element1",
    )

    incompatible_element = models.ForeignKey(
        "RoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент 2",
        related_name="incompatibilities_as_element2",
    )

    class Meta:
        verbose_name = "Несовместимые элементы"
        verbose_name_plural = "Несовместимые элементы"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["element", "incompatible_element"],
                name="unique_incompatibility",
            )
        ]

    def __str__(self):
        return (
            f"Элементы {self.element_id} и {self.incompatible_element_id} несовместимы"
        )


class RoomElementAssignment(models.Model):
    def __str__(self):
        return f"Комната {self.room_id} - элемент {self.element_id}"
    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        verbose_name="Комната",
    )

    element = models.ForeignKey(
        "RoomElement",
        on_delete=models.CASCADE,
        verbose_name="Элемент",
    )

    class Meta:
        verbose_name = "Связь комната-элемент"
        verbose_name_plural = "Связи комната-элемент"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["room", "element"],
                name="unique_room_element_assignment",
            )
        ]