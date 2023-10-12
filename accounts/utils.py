from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination_items(request, items, result):
    page = request.GET.get('page')
    paginator = Paginator(items, result)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        items = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        items = paginator.page(page)

    left_index = (int(page) - 3)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 3)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return custom_range, items