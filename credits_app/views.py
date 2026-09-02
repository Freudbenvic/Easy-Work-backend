from rest_framework import generics, permissions
from .serializers import CreditSerializer


class MyCreditView(generics.RetrieveAPIView):
    """GET /api/credits/me/"""

    serializer_class = CreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.credit
