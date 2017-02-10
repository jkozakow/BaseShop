from django.db import models
from authentication.models import CustomUser
from django.core.validators import MinValueValidator
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager


class BaseManufacturer(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30)

    class Meta:
        abstract = True
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return self.name


class BaseProduct(PolymorphicModel):
    name = models.CharField(verbose_name='Name/model', max_length=30)

    price = models.FloatField(verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity', validators=[MinValueValidator(0)])

    recommended = models.BooleanField(default=False)  # recommended products are show on home page

    additional_spec = models.CharField(verbose_name='Additional specifications', max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PolymorphicManager()

    class Meta:
        db_table = 'products'
        verbose_name = 'Base Product'
        verbose_name_plural = 'Base Products'

    def __str__(self):
        return self.name


class BaseComponent(models.Model):
    name = models.CharField(verbose_name='Name/model', max_length=30)

    class Meta:
        abstract = True
        verbose_name = 'Component'
        verbose_name_plural = 'Components'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(to=CustomUser, verbose_name='User', blank=True, null=True)
    order_number = models.AutoField(verbose_name='Order number', primary_key=True)
    shipping_address = models.TextField('Shipping Address')

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total = 0
        for product in self.order_items.all():
            total += product.total_price
        return total

    @staticmethod
    def create_from_cart(request, form=None):
        products = BaseProduct.objects.filter(pk__in=list(request.session['cart'].keys()))
        for product in products:
            if product.quantity < request.session['cart'][str(product.pk)]:
                raise Exception  # TODO: raise something useful
        if hasattr(request.user, 'address'):
            order = Order(user=request.user, shipping_address=request.user.address)
        else:
            order = Order(shipping_address='%s %s \n %s' % (form.data['first_name'],
                                                            form.data['last_name'],
                                                            form.data['address']))
        order.save()
        for product in products:
            order_item = OrderItem(order=order, product=product, quantity=request.session['cart'][str(product.pk)])
            order_item.save()
            product.quantity -= order_item.quantity
            product.save()

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'User: %s | Order ID: %s | Date: %s' % (self.user, self.order_number,
                                                       self.created_at.strftime("%a, %d %b %Y %H:%M:%S"))


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, verbose_name='Order', related_name='order_items')
    product = models.ForeignKey(to=BaseProduct, verbose_name='Product')
    quantity = models.IntegerField(verbose_name='Quantity')

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return 'Product: %s | Quantity: %s' % (self.product, self.quantity)


class TVManufacturer(BaseManufacturer):

    class Meta:
        db_table = 'tv_manufacturer'

TV_RES_CHOICES = (
    ('1366 x 768', 'HD'),
    ('1920 x 1080', 'Full HD'),
    ('3840 x 2160', 'Ultra HD 4K')
)


class TV(BaseProduct):
    manufacturer = models.ForeignKey(to=TVManufacturer, verbose_name='Manufacturer')
    diagonal = models.CharField(verbose_name='Diagonal', max_length=30, help_text='[inch]')
    resolution = models.CharField(verbose_name='Resolution', max_length=30, choices=TV_RES_CHOICES)

    class Meta:
        db_table = 'tv'
        verbose_name = 'TV'
        verbose_name_plural = 'TVs'

    def __str__(self):
        return '%s %s' % (self.manufacturer, self.name)


class ProcessorManufacturer(BaseManufacturer):

    class Meta:
        db_table = 'processor_manufacturer'


class Processor(BaseComponent):
    manufacturer = models.ForeignKey(to=ProcessorManufacturer, verbose_name='Manufacturer')
    clock_frequency = models.CharField(verbose_name='Clock frequency', max_length=30)
    additional_spec = models.CharField(verbose_name='Additional specifications', max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'processor'
        verbose_name = 'Processor'
        verbose_name_plural = 'Processors'


GRAPHIC_CARD_MANUFACTURER_CHOICES = (
    ('Nvidia', 'Nvidia'),
    ('AMD', 'AMD'),
    ('Intel', 'Intel')
)


class GraphicCard(BaseComponent):
    manufacturer = models.CharField(choices=GRAPHIC_CARD_MANUFACTURER_CHOICES, max_length=30)
    additional_spec = models.CharField(verbose_name='Additional specifications', max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'graphic_card'
        verbose_name = 'Graphic card'
        verbose_name_plural = 'Graphic cards'


class LaptopManufacturer(BaseManufacturer):

    class Meta:
        db_table = 'laptop_manufacturer'


class Laptop(BaseProduct):
    manufacturer = models.ForeignKey(to=LaptopManufacturer, verbose_name='Manufacturer')
    processor = models.ForeignKey(to=Processor, verbose_name='Processor', blank=True, null=True)
    ram = models.CharField(verbose_name='RAM', max_length=30)
    disk = models.CharField(verbose_name='Disk', max_length=30)
    graphic_card = models.ForeignKey(to=GraphicCard, verbose_name='Graphic card', blank=True, null=True)
    diagonal = models.CharField(verbose_name='Diagonal', max_length=30)

    class Meta:
        db_table = 'laptop'
        verbose_name = 'Laptop'
        verbose_name_plural = 'Laptops'

    def __str__(self):
        return '%s %s' % (self.manufacturer, self.name)


class PhoneManufacturer(BaseManufacturer):

    class Meta:
        db_table = 'phone_manufacturer'


class Phone(BaseProduct):
    manufacturer = models.ForeignKey(to=PhoneManufacturer, verbose_name='Manufacturer')
    diagonal = models.CharField(verbose_name='Diagonal', max_length=30)
    resolution = models.CharField(verbose_name='Resolution', max_length=30)
    processor = models.ForeignKey(to=Processor, verbose_name='Processor', blank=True, null=True)
    ram = models.CharField(verbose_name='RAM', max_length=30)
    system = models.CharField(verbose_name='System', max_length=30)

    class Meta:
        db_table = 'phone'
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'

    def __str__(self):
        return '%s %s' % (self.manufacturer, self.name)
