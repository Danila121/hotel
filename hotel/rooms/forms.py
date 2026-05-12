from django import forms


# class ElementSelectionForm(forms.Form):
#     elements = forms.ModelMultipleChoiceField(
#         queryset=RoomElement.objects.all(),
#         widget=forms.SelectMultiple(attrs={
#             'class': 'select2-multiple',
#             'style': 'width: 100%',
#         }),
#         label='Выберите желаемые элементы',
#         required=True,
#     )

#     def clean_elements(self):
#         selected = self.cleaned_data.get('elements')
#         if not selected:
#             return selected

#         # Собираем список пар (id1, id2) для быстрой проверки
#         incompatibilities = IncompatibleRoomElement.objects.values_list(
#             'element_id', 'incompatible_element_id'
#         )

#         selected_ids = set(elem.id for elem in selected)
#         conflicts = []

#         for e1_id, e2_id in incompatibilities:
#             if e1_id in selected_ids and e2_id in selected_ids:
#                 # Получаем названия элементов для читаемого сообщения
#                 name1 = RoomElement.objects.get(pk=e1_id).name
#                 name2 = RoomElement.objects.get(pk=e2_id).name
#                 conflicts.append(f'«{name1}» и «{name2}»')

#         if conflicts:
#             raise forms.ValidationError(
#                 'Выбраны несовместимые элементы: ' + '; '.join(conflicts)
#             )

#         return selected