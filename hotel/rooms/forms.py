from django import forms
from .models import Room, RoomElement, IncompatibleRoomElement


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['price_category']


class RoomElementForm(forms.ModelForm):
    class Meta:
        model = RoomElement
        fields = ['name', 'min_price_category', 'room_id', 'is_required']

        def clean(self):
            cleaned_data = super().clean()
            room = cleaned_data.get('room_id')

            if self.instance.pk:
                original = RoomElement.objects.get(pk=self.instance.pk)

                if original.room_id and original.room_id != room:
                    raise forms.ValidationError(
                        "Этот элемент уже привязан к другой комнате "
                        "и не может быть перемещён."
                    )

            return cleaned_data


class IncompatibleRoomElementForm(forms.ModelForm):
    class Meta:
        model = IncompatibleRoomElement
        fields = '__all__'
