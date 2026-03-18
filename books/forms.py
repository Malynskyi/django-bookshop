from books.models import Meeting
from django import forms
from datetime import timedelta, datetime, timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = '__all__'
        widgets = {
            'schedule': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                     'min': datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M')
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 4:
            raise forms.ValidationError('The name must be longer than 4 characters!')
        return title
    
def clean_schedule(self):
    schedule = self.cleaned_data['schedule']
    current_dt = datetime.now(tz=timezone.utc)
    if current_dt > schedule:
        raise forms.ValidationError(
            f"The date and time cannot be earlier than {current_dt.strftime('%Y-%m-%dT%H:%M')}"
        )
    return schedule


class QueryFilterForm(forms.Form):
    query = forms.CharField(
        label='Title',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class AuthorFilterForm(forms.Form):
     author = forms.ModelChoiceField(
        label='Author',
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
     )

class FilterBookForm(QueryFilterForm, AuthorFilterForm):
    pass