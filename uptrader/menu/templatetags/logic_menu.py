from django import template

from ..models import TreeMenu


register = template.Library()


def recurs_find(tree_menu, pk, result_menu, pre_pk=None):
    """функция начинает идти от стартового узла, поднимается вверх до первого уровня вложенности,
    после чего возвращает структуру описывающую меню для рендера HTML"""

    mid_menu = []
    new_pk = None
    # Перебираем все ветки в поисках уровня родителя для активного пункта меню
    for tree in tree_menu:
        if tree.parent_id == pk:
            mid_menu.append(tree)

        # Параллельно ищем id родителя нынешнего уровня для следующей итерации
        if tree.id == pk:
            new_pk = tree.parent_id

    result_menu.insert(0, (mid_menu, pre_pk))
    # В случае если есть куда подниматься дальше по веткам запускаем рекурсию, в обратном случае прерываем
    if pk:
        return recurs_find(tree_menu, new_pk, result_menu=result_menu, pre_pk=int(pk))
    return result_menu


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name_menu):
    # Когда идёт рекурсивная проходка по сформированной в виде [] структуре меню,
    # отвечает за открытие последующих уровней последущего уровня вложенности
    if type(name_menu) is list:
        noda = name_menu[1][1]
        return {'tree_menu': name_menu[1:],
                'signature_node': noda}

    menu_data = context['request'].GET.get("menu", "")
    pk = context['request'].GET.get("pk", None)

    # Если сейчас не ведётся работа с конкретным меню или нет запроса на уровень вложности,
    # запускается рендер меню с нулем уровнем вложенности
    if menu_data != name_menu or pk is None:
        tree_menu = TreeMenu.objects.select_related("menu").filter(menu=name_menu, parent=None)
        return {'tree_menu': [(tree_menu, None)],
                'signature_node': None}

    # Производит сборку данных для рендера меню по заданному узлу
    tree_menu = TreeMenu.objects.select_related("menu").filter(menu=name_menu)
    result_menu = recurs_find(tree_menu, int(pk), [])
    print(result_menu)
    return {'tree_menu': result_menu,
            'signature_node': result_menu[0][1]}
