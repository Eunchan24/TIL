from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['app_list'] = ['polls', 'boos']
        return  context