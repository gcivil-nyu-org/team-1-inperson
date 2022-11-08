from django import forms
from django.forms import ModelForm
from report.models import Report


class ReportForm(ModelForm):
    comment = forms.CharField(label="comment", max_length=100)

    class Meta:
        model = Report
        fields = [
            "reportID",
            "user",
            "infraID",
            "comment",
            "isResolved",
            "dateTimeOfResolution",
        ]
