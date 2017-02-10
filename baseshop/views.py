from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from rest_framework.viewsets import generics
from baseshop.models import BaseProduct, Order, TV, Laptop, Phone
from baseshop.forms import AnonymousOrderForm, ProductsSearchForm
from baseshop.serializers import ProductSerializer
from authentication.forms import LoginForm


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = BaseProduct.objects.filter(recommended=True)
        context['products'] = products
        context['form'] = ProductsSearchForm
        return context


class BaseProductDetailView(DetailView):
    template_name = 'detail.html'
    detail_list = []

    def get_context_data(self, **kwargs):
        ret = super(BaseProductDetailView, self).get_context_data(**kwargs)

        ret.update({
            'detail_list': self.detail_list,
        })
        return ret


class BaseCategoryView(ListView):
    template_name = 'list.html'
    detail_list = []

    def get_context_data(self, **kwargs):
        ret = super(BaseCategoryView, self).get_context_data(**kwargs)

        ret.update({
            'detail_list': self.detail_list,
        })
        return ret


class LaptopCategoryView(BaseCategoryView):
    model = Laptop
    detail_list = ['price', 'processor', 'ram', 'graphic_card', 'disk', 'additional_spec']


class TVCategoryView(BaseCategoryView):
    model = TV
    detail_list = ['price', 'diagonal', 'resolution', 'additional_spec']


class PhoneCategoryView(BaseCategoryView):
    model = Phone
    detail_list = ['price', 'diagonal', 'resolution', 'processor', 'ram', 'system', 'additional_spec']


class LaptopDetailView(BaseProductDetailView):
    model = Laptop
    detail_list = ['name', 'processor', 'ram', 'disk', 'graphic_card', 'additional_spec']


class TVDetailView(BaseProductDetailView):
    model = TV
    detail_list = ['name', 'diagonal', 'resolution', 'additional_spec']


class PhoneDetailView(BaseProductDetailView):
    model = Phone
    detail_list = ['name', 'diagonal', 'resolution', 'processor', 'ram', 'system', 'additional_spec']


class RESTProductDetail(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return BaseProduct.objects.filter(pk=self.kwargs['pk'])


class CartListView(ListView):
    model = BaseProduct
    template_name = 'cart.html'

    def get_queryset(self):
        if 'cart' in self.request.session:
            return self.model.objects.filter(pk__in=list(self.request.session['cart'].keys()))


class OrdersListView(ListView):
    model = Order
    template_name = 'orders.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise Http404
        return super(OrdersListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.all().order_by('completed')
        else:
            return self.model.objects.filter(user=self.request.user)


class ChooseOrderOptionsView(TemplateView):
    template_name = 'order_options.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/confirm_order')
        return super(ChooseOrderOptionsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChooseOrderOptionsView, self).get_context_data(**kwargs)
        context['form'] = LoginForm
        return context


class AnonymousOrderView(ListView, FormMixin):
    model = BaseProduct
    template_name = 'anon_order.html'
    form_class = AnonymousOrderForm

    def get_queryset(self):
        return self.model.objects.filter(pk__in=list(self.request.session['cart'].keys()))

    def post(self):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ConfirmOrder(ListView):
    model = BaseProduct
    template_name = 'confirm_order.html'

    def get_queryset(self):
        return self.model.objects.filter(pk__in=list(self.request.session['cart'].keys()))


def create_order_view(request):
    try:
        Order.create_from_cart(request)
        request.session['cart'] = {}
    except Exception as e:  # TODO: use less broad exception
        return HttpResponseRedirect('/fail/')
    else:
        return HttpResponseRedirect('/order_success/')


def create_anonymous_order(request):
    form = AnonymousOrderForm()
    try:
        form = AnonymousOrderForm(data=request.POST)
        if form.is_valid():
            Order.create_from_cart(request, form)
            request.session['cart'] = {}
    except Exception as e:
        return HttpResponseRedirect('/fail/')
    else:
        return HttpResponseRedirect('/order_success/')


def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    if item_id not in cart:
        cart[item_id] = 1
    else:
        cart[item_id] += 1
    request.session['cart'] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def del_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart and cart[item_id] > 1:
        cart[item_id] -= 1
    else:
        del cart[item_id]
    request.session['cart'] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
