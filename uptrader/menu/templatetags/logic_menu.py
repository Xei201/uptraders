import re

from django import template
from django.http import HttpRequest
from django.template import RequestContext
from django.urls import reverse, NoReverseMatch

from ..models import TreeMenu

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name_menu):
    menu_data = context['request']["GET"].get("name_menu", "")
    pk = context['request']["GET"].get("pk", "")

    if menu_data != name_menu:
        tree_menu = TreeMenu.objects.filter(nemu=name_menu)
        return {'tree_menu': tree_menu,
                'signature_node': None}







    if parent != 0 and 'menu' in context:
        menu = context['menu']
    else:

        is_url = re.compile(r'^http[s]?://')

        # Get path if request exist
        current_path = context['request'].path \
            if 'request' in context and isinstance(context['request'], HttpRequest) \
            else ''

        data = TreeMenu.objects.select_related()\
            .filter(category__name=name)\
            .order_by('pk')

        menu = []

        for item in data:

            path = item.path.strip()

            target = '_self'

            if is_url.match(path):
                url = path
                target = '_blank'
            else:
                try:
                    url = reverse(path)
                except NoReverseMatch:
                    url = path

            menu.append({
                'id': item.pk,
                'url': url,
                'target': target,
                'name': item.name,
                'parent': item.parent_id or 0,
                'active': True if url == current_path else False,
            })

    return {
        'menu': menu,
        'current_menu': (item for item in menu if 'parent' in item and item['parent'] == parent),
    }