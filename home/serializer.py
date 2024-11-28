from rest_framework.serializers import ModelSerializer
from home.models import *


class paymentserializer(ModelSerializer):
    class Meta:
        model=payment
        fields="__all__"

        