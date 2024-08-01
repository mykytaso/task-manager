from datetime import date

from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import (
    Task,
    TaskPriority,
    TaskType,
)


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=date.today(),
    )

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        empty_label="Choose Type",
    )

    priority = forms.ModelChoiceField(
        empty_label="Choose Priority",
        queryset=TaskPriority.objects.all(),
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by task name",
            }
        ),
    )


class WorkerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by username",
            }
        ),
    )
