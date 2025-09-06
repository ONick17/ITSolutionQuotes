from django import forms
from main.models import Quote
from django.core.exceptions import ValidationError



class QuoteForm(forms.ModelForm):
    delete = forms.BooleanField(
        required=False,
        initial=False,
        label="Удалить эту цитату"
    )


    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['text'].disabled = True
            self.fields['source'].disabled = True


    def clean_text(self):
        text = self.cleaned_data["text"]
        qs = Quote.objects.filter(text=text)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            # raise forms.ValidationError("Такая цитата уже существует.")
            self.add_error("text", "Такая цитата уже существует.")
        return text


    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")

        if not self.instance.pk and source:
            if Quote.objects.filter(source=source).count() >= 3:
                # raise ValidationError("Нельзя добавить больше 3 цитат из одного источника.")
                self.add_error("source", "Нельзя добавить больше 3 цитат из одного источника.")

        return cleaned_data
