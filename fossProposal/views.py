from django.shortcuts import render
from django.views.generic.list import ListView
from django.utils import timezone

from .models import Proposal

# Create your views here.

class ProposalListView(ListView):

    model = Proposal



def proposal_list(request):
    return render(request, 'fossProposal/proposal_list.html', {})

def proposal_add(request):
    return render(request, 'fossProposal/proposal_add.html', {})

