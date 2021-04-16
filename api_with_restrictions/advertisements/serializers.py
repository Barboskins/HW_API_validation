from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        print(validated_data)

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    # @action(detail=True, methods=['post', 'patch'])
    def validate(self, data):
        # print(self.context["view"].action)
        all_posts_status = Advertisement.objects.filter(status="OPEN").all()
        if len(all_posts_status) >= 10:
            raise serializers.ValidationError("Превышено количество открытых объявлений")


        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        return data

