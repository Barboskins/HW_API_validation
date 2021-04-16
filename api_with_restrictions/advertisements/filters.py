from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    creator = filters.ModelMultipleChoiceFilter(field_name='id',to_field_name='id',
                                                queryset=Advertisement.objects.all())
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры

    class Meta:
        model = Advertisement
        fields = ['created_at']
