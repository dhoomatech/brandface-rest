# cards/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class KeywordSuggestionAPIView(APIView):
    """
    Accepts a business name and returns keyword suggestions.
    """
    def get(self, request):
        business_name = request.query_params.get('name')
        if not business_name:
            return Response({"error": "Missing business name"}, status=status.HTTP_400_BAD_REQUEST)

        # Call Twinword API
        try:
            twinword_api_key = "YOUR_API_KEY"
            url = "https://api.twinword.com/api/keyword/suggestion/"
            headers = {
                "X-Twaip-Key": twinword_api_key
            }
            params = {
                "entry": business_name
            }
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if response.status_code != 200:
                return Response({"error": data.get("message", "API error")}, status=response.status_code)

            return Response({
                "keywords": data.get("keyword", []),
                "source": "Twinword"
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
