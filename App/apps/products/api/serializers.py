from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(style={'base_template':'textarea.html'})
    price = serializers.DecimalField()
    image = serializers.ImageField()

    def validate_name(self,value):
        pass

    def validate_email(self,value):
        pass

    def validate(self,data):
        pass

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        return super().update(instance, validated_data)
    
    def save(self):
        pass

    def to_representation(self, instance):
        return super().to_representation(instance)