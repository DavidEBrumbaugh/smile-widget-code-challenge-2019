from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class ProductAPITests(APITestCase):
    fixtures = ['0001_fixtures']

    def test_required_parameters(self):
        """
        Ensure we enforce required parameters.
        """
        url = reverse('get-price')
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        url += '?productCode=sm_widget'
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_date_format(self):
        """
        Ensure we enforce date format
        """
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=January+1+2019'
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_normal_2018_prices(self):
        """
        Ensure Correct prices for 2018 without GiftCard
        """
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2018-01-01'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$99.00')

    def test_black_friday(self):
        """
        Ensure Correct Black Friday prices
        """
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2018-11-23'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$0.00')
        url = reverse('get-price')
        url += '?productCode=big_widget&date=2018-11-23'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$800.00')

    def test_normal_2019_prices(self):
        """
        Ensure Correct prices for 2019 without GiftCard
        """
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2019-02-01'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$125.00')
        url = reverse('get-price')
        url += '?productCode=big_widget&date=2019-02-23'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$1200.00')

    def test_gift_cards(self):
        """
        Check Prices with giftCardCode
        """
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2019-02-01&giftCardCode=50OFF'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$75.00')

        # Out of Date Range
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2019-02-01&giftCardCode=250OFF'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$125.00')

        # In Date Range
        url = reverse('get-price')
        url += '?productCode=big_widget&date=2018-12-25&giftCardCode=250OFF'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$750.00')

        # In Date Range but More than Price
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2018-12-25&giftCardCode=250OFF'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$0.00')

    def test_black_friday_gift_cards(self):
        """
        Make sure gift cards work right on black friday
        """
        url = reverse('get-price')
        url += '?productCode=sm_widget&date=2018-11-23&giftCardCode=50OFF'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$0.00')

        url = reverse('get-price')
        url += '?productCode=big_widget&date=2018-11-23&giftCardCode=10OFF'
        response = self.client.get(url,format='json')
        self.assertIs('price' in response.data, True )
        self.assertEqual(response.data['price'],'$790.00')
