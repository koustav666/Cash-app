from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from payment.models import Currency

@api_view(["GET"])
def currency_conversion(request, currency1, currency2, amount_of_currency1):
    try:
        amount_of_currency1 = Decimal(amount_of_currency1)  # Convert to Decimal for accuracy
    except:
        return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch currency objects from database
    currency1_obj = get_object_or_404(Currency, code=currency1.upper())
    currency2_obj = get_object_or_404(Currency, code=currency2.upper())

    # Calculate conversion rate
    conversion_rate = currency2_obj.value / currency1_obj.value
    converted_amount = amount_of_currency1 * conversion_rate

    return Response({
        "currency1": currency1.upper(),
        "currency2": currency2.upper(),
        "amount_of_currency1": amount_of_currency1,
        "conversion_rate": round(conversion_rate, 4),
        "converted_amount": round(converted_amount, 4)
    })
