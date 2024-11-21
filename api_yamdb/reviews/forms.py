import datetime as dt
from django.core.exceptions import ValidationError
from django import forms

from reviews.models import Title, Review


class TitleForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = '__all__'

    def clean(self):
        data = super().clean()
        if data.get('year') > dt.datetime.now().year:
            raise ValidationError(
                'Год выпуска не может быть больше текущего.'
            )


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            queryset=Title.objects.all(), label='Произведение')

    def clean(self):
        data = super().clean()
        value = data.get('score')
        if value < 1 or value > 10:
            raise ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10'
            )
