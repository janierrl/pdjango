from django import forms
from ...models.search import Search
from ...config import LANGUAGES

class SearchForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGES.items(), label='Language')

    class Meta:
        model = Search
        fields = ["title", "language"]
