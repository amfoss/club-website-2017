from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# models
from fosster.models import Subscription


class AuthorCreate(CreateView):
    template_name = 'fosster/coming_soon/coming-soon.html'
    model = Subscription
    fields = ['name', 'email']
    success_url = '/fosster/thank_you'

    def form_valid(self, form):

        return super(AuthorCreate, self).form_valid(form)


class ThankYou(TemplateView):
    template_name = 'fosster/coming_soon/thank-you.html'
