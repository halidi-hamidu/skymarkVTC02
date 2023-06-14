from rest_framework import serializers
from skymarkApp.models import ManageClass


class ManageClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = ManageClass
        fields = '__all__'
