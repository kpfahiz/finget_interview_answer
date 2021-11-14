from rest_framework.serializers import  ModelSerializer, PrimaryKeyRelatedField

from .models import (
                Item,
                Invoice,
                )
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class InvoiceSerializer(ModelSerializer):
    
    user = UserSerializer()
    items = ItemSerializer()
    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        user_date = validated_data.pop('user')
        item_data = validated_data.pop('items')
        items = Item.objects.create(**item_data)
        user = User.objects.create(**user_date)
        invoice = Invoice.objects.create(user=user,items=items,**validated_data)
        return invoice


