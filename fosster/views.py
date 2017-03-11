from django.views.generic import TemplateView

# Create your views here.


class ComingSoon(TemplateView):
    template_name = 'fosster/coming_soon/coming-soon.html'
