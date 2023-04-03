from django import template

from ..models import TreeMenu


register = template.Library()


def recurs_find(tree_menu, pk, result_menu, pre_pk=None):
    mid_menu = []
    del_list = []
    new_pk = None
    for index in range(len(tree_menu)):
        if tree_menu[index]["parent"] == int(pk):
            mid_menu.append(tree_menu[index])
            del_list.addend(index)

        if tree_menu[index]["id"] == int(pk):
            new_pk = tree_menu[index]["parent"]

    result_menu.insert(0, (mid_menu, pre_pk))
    if new_pk:
        for item in del_list:
            tree_menu.pop(item)
        return recurs_find(tree_menu, new_pk, result_menu=result_menu, pre_pk=pk)
    return result_menu


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name_menu):
    if type(name_menu) is list:
        noda = name_menu[1][1]
        return {'tree_menu': name_menu[1:],
                'signature_node': noda}

    menu_data = context['request'].GET.get("name_menu", "")
    pk = context['request'].GET.get("pk", None)

    if menu_data != name_menu or pk is None:
        tree_menu = TreeMenu.objects.filter(menu=name_menu, parent=None)
        return {'tree_menu': [(tree_menu, None)],
                'signature_node': None}

    tree_menu = TreeMenu.objects.all().values()
    result_menu = recurs_find(tree_menu, pk, [])
    return {'tree_menu': result_menu,
            'signature_node': result_menu[0][1]}
