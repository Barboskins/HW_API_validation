from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def destroy(self, request, pk=None):
        ad = self.get_object() #объявление с полями
        user = request.user #пользователь, который хочет удалить
        if user == ad.creator:  #проверка с автором объявления
            self.perform_destroy(ad)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Удаление невозможно. Вы не являетесь автором объявления',status=status.HTTP_403_FORBIDDEN)


