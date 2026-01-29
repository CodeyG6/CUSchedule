from django import forms
from .models import Professor
from .models import Course

class ProfessorDataSearch(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'
        labels = {
            'name': 'Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'exProfName', 'class':'form-control'})
        }

class CourseSearch(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        labels = {
            'CourseNumber': 'Course Number',
            'Honors': 'Honors',
            'Subject': 'Subject',
            'MeetingDays': 'Meeting Days',
            'PassRate': 'Pass Rate',
            'StartTime': 'Start Time',
            'EndTime': 'End Time'
        }
        widgets = {
            'coursenumber': forms.TextInput(attrs={'placeholder': 'e.g., 1010', 'class': 'form-control'}),
            'honors': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., MATH', 'class': 'form-control'}),
            'meetingdays': forms.TextInput(attrs={'placeholder': 'e.g., MWF', 'class': 'form-control'}),
            'passrate': forms.NumberInput(attrs={'placeholder': 'e.g., 85.0', 'class': 'form-control'}),
            'starttime': forms.TextInput(attrs={'placeholder': 'e.g., 8:00AM', 'class': 'form-control'}),
            'endtime': forms.TextInput(attrs={'placeholder': 'e.g., 8:00PM', 'class': 'form-control'})
        }