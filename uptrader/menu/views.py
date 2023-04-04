from django.views import generic


class TestView(generic.TemplateView):
    """Генерирует тестовую страницу для меню"""

    template_name = "general.html"
