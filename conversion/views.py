from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Hardcoded currency exchange rates
EXCHANGE_RATES = {
    "USD": {
        "EUR": 0.93,
        "GBP": 0.80,
    },
    "EUR": {
        "USD": 1.08,
        "GBP": 0.86,
    },
    "GBP": {
        "USD": 1.25,
        "EUR": 1.16,
    },
}


@api_view(['GET'])
def convert_currency(request, currency1, currency2, amount_of_currency1):
    try:
        amount_of_currency1 = float(amount_of_currency1)  # Convert to float
        rate = EXCHANGE_RATES[currency1][currency2]
        conversion_result = rate * amount_of_currency1
        return Response({"converted_amount": conversion_result})
    except ValueError:
        return Response({"error": "Invalid amount provided."}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({"error": "One or both currencies are not supported."}, status=status.HTTP_400_BAD_REQUEST)
