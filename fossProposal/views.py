from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Proposal

# Create your views here.

class ProposalListView(ListView):

    model = Proposal


class ProposalCreate(CreateView):

    model = Proposal
    fields = ['title']

