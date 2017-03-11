from django.views.generic import TemplateView

# Create your views here.

class CommingSoon(TemplateView):
    template_name = 'fosster/coming_soon/coming_soon.html'
