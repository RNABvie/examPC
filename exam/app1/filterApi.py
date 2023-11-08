from django_filters import FilterSet
from .models import User

class UserInfoFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['exact', 'contains'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'id': ['exact']
        }