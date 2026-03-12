from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title','description','deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control mb-2'})


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text','time_limit','media']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control mb-2'})


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text','is_correct']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control mb-2'})
        self.fields['is_correct'].widget.attrs.update({'class':'form-check-input'})


AnswerFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=4, can_delete=True
)