from django import forms

class CreateArticle(forms.Form):
    title = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    synopsis = forms.CharField(max_length=312, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), required=True)
