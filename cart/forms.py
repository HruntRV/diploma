from django import forms
from django.utils.html import format_html

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if self.product and quantity > self.product.stock:  # Assuming product has a 'stock' field
            raise forms.ValidationError(
                format_html("<b>Доступно {} шт.</b>", self.product.stock),
                code='invalid'
            )
        return quantity
