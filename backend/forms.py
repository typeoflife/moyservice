from django import forms

from backend.models import Order, Entry, Cash


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['device', 'model', 'serial_number']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = ['name']
        labels = {'name': ''}


class SumForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['sum']
        labels = {'sum': ''}
