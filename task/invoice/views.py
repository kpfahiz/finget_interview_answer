from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

import datetime

from .helper import save_pdf

from .models import Invoice, Item
from .serializers import InvoiceSerializer


class ItemViewSet(ListCreateAPIView):
    """
    A viewset for viewing and editing Invoice instances.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class GeneratePdf(APIView):
    """
    A viewset GeneratePdf for Download Invoice of  instances.
    """
    def get(self, request, id):
        invoices = Invoice.objects.filter(id=id).values()
        invoice_id = invoices[0]['id']
        invoice_date = invoices[0]['date']
        invoice_user = User.objects.filter(id=invoices[0]['user_id']).values()
        invoice_user_name = invoice_user[0]['username']
        invoice_items = Item.objects.filter(invoice__id=invoice_id).values()
        invoice_item_name = invoice_items[0]['name']
        invoice_item_price = invoice_items[0]['unit_price']
        discount = 5
        total_price = invoice_item_price - (invoice_item_price * discount / 100)
        invoice_item_quantity = invoice_items[0]['quantity']
        invoice_item_tax = invoice_items[0]['tax']/100
        total_price_without_tax = invoice_item_price * invoice_item_quantity
        total_price_with_tax = total_price+(total_price * invoice_item_tax)
        
        context = {
            'invoice_date': invoice_date,
            'invoice_user_name': invoice_user_name,
            'invoice_item_name': invoice_item_name,
            'invoice_item_price': invoice_item_price,
            'invoice_item_quantity': invoice_item_quantity,
            'invoice_item_tax': invoice_item_tax,
            'tax': invoice_item_tax,
            'total_price_without_tax': total_price_without_tax,
            'total_price_with_tax': total_price_with_tax,
            'discount': discount,
            'total_price': total_price,
        }
        file_name , status = save_pdf(context)

        if status:
            return Response({'status': 200,'path': f'/media/{file_name}'})
        return Response({'status': 200})