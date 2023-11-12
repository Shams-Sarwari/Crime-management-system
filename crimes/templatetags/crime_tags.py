from django import template
from ..models import CarCrime
from django.db.models import Q


register = template.Library()

@register.simple_tag
def total_notifications(request):
    pending_crimes = CarCrime.objects.filter(
        Q(pending=True) &
        Q(province=request.user.staffprofile.work_place.province)
        )
    return pending_crimes.count()