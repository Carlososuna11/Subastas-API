from rest_framework import serializers
from apps.pinturas.api.serializers.pintura import PinturaSerializer
from apps.monedas.api.serializers.moneda import MonedaSerializer

class CatalogoSerializer(serializers.Serializer):
    pinturas = PinturaSerializer(many=True)
    monedas = MonedaSerializer(many=True)
