from django import forms
from .models import Product
from django.core.validators import FileExtensionValidator

MAX_IMAGE_SIZE = 5 * 1024 * 1024
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):


    class Meta:
        model = Product
        fields = ("name_product", "description", "image", "category", "price")

    image = forms.ImageField(
        required=False,
        label='Изображение',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ],
        error_messages={
            'invalid_image': 'Загрузите корректное изображение (JPEG или PNG).',
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_product'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['image'].widget.attrs.update({'class': 'form-control','accept': 'image/jpeg,image/png',})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})


    def clean_name_product(self):
        name_product = self.cleaned_data['name_product'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name_product:
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии')
        return name_product

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено в описании')
        return description
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    


    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > self.MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                "Размер изображения не должен превышать 5 МБ."
            )
        return image