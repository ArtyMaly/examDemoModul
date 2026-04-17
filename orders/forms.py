from django import forms
from .models import Order


class OrderClientForm(forms.ModelForm):
    """Форма для клиента: создание заказа"""
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'product': 'Товар',
            'quantity': 'Количество',
            'notes': 'Примечания',
        }


class OrderManagerForm(forms.ModelForm):
    """Форма для менеджера: обновление статуса и примечаний"""
    class Meta:
        model = Order
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'status': 'Статус',
            'notes': 'Примечания',
        }


class OrderAdminForm(forms.ModelForm):
    """Форма для администратора: полное редактирование"""
    class Meta:
        model = Order
        fields = ['client', 'product', 'quantity', 'status', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'client': 'Клиент',
            'product': 'Товар',
            'quantity': 'Количество',
            'status': 'Статус',
            'notes': 'Примечания',
        }
