from django.forms import ModelForm
from .models import Workplace_Schedule, Meeting_Room_Schedule


class Workplace_ScheduleForm(ModelForm):
    class Meta:
        required_css_class = 'form-control'
        model = Workplace_Schedule
        fields = ['start', 'finish']


class Meeting_Room_ScheduleForm(ModelForm):
    class Meta:
        required_css_class = 'form-control'
        model = Meeting_Room_Schedule
        fields = ['start', 'finish']
