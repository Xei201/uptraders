from django.views import generic


class TestView(generic.TemplateView):
    """Генерирует тестовую страницу для меню"""

    template_name = "menu/general.html"
