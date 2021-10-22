from django import forms
from .models import Todo, Tag

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag):
        return '%s' % tag.title

class TodoForm(forms.ModelForm):
    tags = CustomMMCF(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Todo

        fields = ['title', 'content', 'tags']
        labels = {
            'title': "Your Todo Title",
            'content': 'Your Todo Content',
            'tags': 'Todo\'s Tags'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
