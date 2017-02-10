from django import template
from django.apps import apps
from baseshop.models import BaseProduct

register = template.Library()


@register.inclusion_tag('webtag_templates/display_object_as_dt_list.html')
def webtag_object_as_list(obj, fields):
    """
    Wyswietla obiekt jako wiele elementow dt/dd listy dl

    Uzywa webtags_object_dt do generowania listy
    """

    return {
        'object': obj,
        'fields': fields,
    }


@register.inclusion_tag('webtag_templates/display_object_dt.html')
def webtag_object_dt(obj, field):
    """
    Wyświetla element obiektu jako pojedyncze dt/dd listy dl, wraz z odnośnikiem do obiektu.
    """
    from functools import reduce

    splited_field_name = field.split(".")

    # Pobranie przedostaniego obiektu
    last_obj = reduce(getattr, splited_field_name[:-1], obj)
    # Ostatni obiekt z pola field
    current_obj = reduce(getattr, splited_field_name, obj)

    obj_field = last_obj.__class__._meta.get_field(splited_field_name[-1])

    return {
        'object': {
            'desc': obj_field.verbose_name,
            'value': current_obj,
            'field_name': field,
            'field_type': obj_field.get_internal_type(),
        },
    }


@register.filter
def to_model_name(model):
    return model.__class__.__name__.lower()


@register.inclusion_tag('webtag_templates/cart_product_tag.html')
def cart_quantity(request, product):
    quantity = request.session['cart'][str(product.pk)]

    return {
        'product': product,
        'quantity': quantity,
        'price': product.price,
        'total_price': product.price * quantity
    }


@register.simple_tag
def cart_total(request):
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        return 0
    products = BaseProduct.objects.filter(pk__in=list(cart.keys()))
    price_total = 0
    for product in products:
        price_total += product.price * cart[str(product.pk)]
    return price_total


@register.inclusion_tag('webtag_templates/menu_tag.html')
def menu_tag(request, *products):
    models = []
    for product in products:
        klass = apps.get_model(app_label='baseshop', model_name=product)
        models.append((klass._meta.verbose_name_plural.lower(), klass._meta.verbose_name_plural))
    return {
        'models': models,
        'request': request
    }
