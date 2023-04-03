from django.views import generic


class TestView(generic.TemplateView):
    """Generates a webhook after the end of the webinar on bison"""

    template_name = "menu/general.html"
