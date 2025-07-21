from rest_framework import generics, permissions
from .models import Enquiry
from .serializers import EnquirySerializer

class EnquiryCreateAPIView(generics.CreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
    permission_classes = [permissions.AllowAny]  # 🔓 Public access


class EnquiryListByBusinessView(generics.ListAPIView):
    serializer_class = EnquirySerializer
    permission_classes = [permissions.IsAuthenticated]  # 🔐 Requires token

    def get_queryset(self):
        business_id = self.kwargs.get("business_id")
        user = self.request.user

        return Enquiry.objects.filter(
            business__id=business_id,
            business__user=user
        ).order_by('-created_at')
