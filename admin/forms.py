from django.forms import ModelForm
from django import forms
from django.core.validators import MinValueValidator
from store.models import Products,Collection

class ProductCreationForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                          'placeholder':'Title'}))

    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-lg',
                                                               'placeholder':'Description'}))

    unit_price = forms.DecimalField(max_digits=6,
                                    decimal_places=2,
                                    validators=[MinValueValidator(1)],
                                    widget=forms.NumberInput(attrs={'class':'form-control',
                                                                    'placeholder':'Price'}))
    
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class':'form-control',
                                                         'placeholder':'Slug'}))
    
    inventory = forms.IntegerField(validators=[MinValueValidator(0)],
                                   widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    collection = forms.ModelMultipleChoiceField(queryset = Collection.objects.all(),
                                                widget = forms.Select(attrs={'class':'form-control'}))

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['title','description','unit_price','slug','inventory','collection']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'description':forms.Textarea(attrs={'class':'form-control form-control-lg','placeholder':'Description'}),
            'unit_price':forms.NumberInput(attrs={'class':'form-control','placeholder':'Price'}),
            'slug':forms.TextInput(attrs={'class':'form-control','placeholder':'Slug'}),
            'inventory':forms.NumberInput(attrs={'class':'form-control'}),
            'collection':forms.Select(attrs={'class':'form-control'}),
        }