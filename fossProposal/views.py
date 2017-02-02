from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Proposal

# Create your views here.

class ProposalListView(ListView):

    model = Proposal


class ProposalCreateView(CreateView):

    model = Proposal
    fields = '__all__'

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        return super(ProposalCreateView, self).form_valid(form)
