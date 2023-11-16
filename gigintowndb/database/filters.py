import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    City = django_filters.CharFilter(lookup_expr='iexact')
    State = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Event
        fields = ['City', 'State']