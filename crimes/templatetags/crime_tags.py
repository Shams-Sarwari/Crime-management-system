from django import template
from ..models import CarCrime, Contact, Payment
from django.db.models import Q


register = template.Library()

@register.simple_tag
def total_notifications(request):
    pending_crimes = CarCrime.objects.filter(
        Q(pending=True) &
        Q(province=request.user.staffprofile.work_place.province)
        )
    pending_comments = Contact.objects.filter(read=False)
    return pending_crimes.count() + pending_comments.count()

@register.simple_tag
def total_online_payment(year):
    total_online = 0
    for item in Payment.objects.filter(
        Q(created__year=year) &
        Q(online=True)):
        total_online += item.price 

    return total_online

@register.simple_tag
def total_offline_payment(year):
    total_offline = 0
    for item in Payment.objects.filter(Q(created__year=year) & Q(online=False)):
        total_offline += item.price

    return total_offline

@ register.simple_tag
def total_payment(year):
    return total_online_payment(year) + total_offline_payment(year)