from rest_framework import serializers
from baseshop.models import BaseProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseProduct
        fields = ('id', 'quantity')
