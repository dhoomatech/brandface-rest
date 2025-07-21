from django.urls import path
from .views import EnquiryCreateAPIView,EnquiryListByBusinessView

urlpatterns = [
    path('create/', EnquiryCreateAPIView.as_view(), name='enquiry-create'),
    path('list/<int:business_id>/', EnquiryListByBusinessView.as_view(), name='enquiry-list'),
]
