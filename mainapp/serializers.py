from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import User

class UserSerializer(serializers.ModelSerializer):
    firma = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model=User
        fields=(
            '__all__'
        )

class UserSerializerGet(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(
            '__all__'
        )
            
        