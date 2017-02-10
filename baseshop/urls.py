from django.conf.urls import url
from baseshop import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^laptop/$', views.LaptopCategoryView.as_view(), name='laptops'),
    url(r'^laptop/(?P<pk>[0-9]+)/$', views.LaptopDetailView.as_view()),
    url(r'^tv/$', views.TVCategoryView.as_view(), name='tvs'),
    url(r'^tv/(?P<pk>[0-9]+)/$', views.TVDetailView.as_view()),
    url(r'^phone/$', views.PhoneCategoryView.as_view(), name='phones'),
    url(r'^phone/(?P<pk>[0-9]+)/$', views.PhoneDetailView.as_view()),
    url(r'^product/(?P<pk>[0-9]+)/$', views.RESTProductDetail.as_view()),
    url(r'^add_to_cart/(?P<item_id>[0-9]+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^del_from_cart/(?P<item_id>[0-9]+)/$', views.del_from_cart, name='del_from_cart'),
    url(r'^cart/$', views.CartListView.as_view()),
    url(r'^order_options/$', views.ChooseOrderOptionsView.as_view(), name='order_options'),
    url(r'^confirm_order/$', views.ConfirmOrder.as_view(), name='confirm_order'),
    url(r'^create_order/$', views.create_order_view, name='create_order'),
    url(r'^anon_order/$', views.AnonymousOrderView.as_view()),
    url(r'^anon_form/$', views.create_anonymous_order, name='anon_form'),
    url(r'^order_success/$', views.TemplateView.as_view(template_name='order_success.html'), name='order_success'),
    url(r'^fail/$', views.TemplateView.as_view(template_name='failed.html'), name='fail'),
    url(r'^orders/$', views.OrdersListView.as_view()),
]
