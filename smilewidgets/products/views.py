from django.shortcuts import render, get_object_or_404

# TODO: Check coding standards for order of import
from .models import Product, GiftCard, ProductPrice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q


# Create your views here.
class PriceView(APIView):
     """
     * Accepts a product code, date, and (optional) gift card and returns JSON product price.
     * Live at api/get-price and accepts the following parameters:
        > productCode
        > date
        > giftCardCode

     TODO: Do we need to add authentication before production?
     """
     def get(self, request, format=None):
        # Product must exist
        if 'productCode' not in request.query_params:
            content = {'Missing Parameter': 'productCode'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            product = get_object_or_404(Product, code=request.query_params['productCode'])
            price = product.price

        # Date must exist and be formatted properly
        if 'date' not in request.query_params:
            content = {'Missing Parameter': 'date'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                datep = datetime.strptime(request.query_params['date'], '%Y-%m-%d')
            except:
                content = {'Invalid Date Format': 'Must Be: YYYY-MM-DD'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

            # In case special product price dates have overlap, give the customer the "best" price
            special_price = ProductPrice.objects.filter(Q(product=product),
                Q(date_start__lte=datep),
                Q(date_end__gte=datep) | Q(date_end__isnull=True)).order_by('-price')

            # If special price is found, replace default price
            if special_price.exists():
                price = special_price[0].price;

        # If a GiftCard Code is specified, it must exist and have a valid date range
        if 'giftCardCode' in request.query_params:
            giftcard = GiftCard.objects.filter(Q(code=request.query_params['giftCardCode']),
                Q(date_start__lte=datep),
                Q(date_end__gte=datep) | Q(date_end__isnull=True))

            # The discount cannot exceed the price
            if giftcard.exists():
                if giftcard[0].amount <= price:
                    price -= giftcard[0].amount
                else:
                    price = 0

        formatted_price = '${0:.2f}'.format(price / 100)

        return Response({"price": formatted_price})
