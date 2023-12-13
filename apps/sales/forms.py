from django import forms

class OrderCreateForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=1)