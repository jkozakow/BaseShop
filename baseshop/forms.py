from django import forms
from haystack.forms import SearchForm


class AnonymousOrderForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'}))
    last_name = forms.CharField(label="Last name", max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10, 'class': 'form-control',
                                                           'name': 'address'}))


class ProductsSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
