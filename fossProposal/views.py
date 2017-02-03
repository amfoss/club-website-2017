from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from fossWebsite.helper import get_session_variables
from .models import Proposal
from register.models import User_info

# Create your views here.

class ProposalListView(ListView):

    model = Proposal


class ProposalCreateView(CreateView):

    model = Proposal
    fields = '__all__'

    def form_valid(self, form):
        is_loggedin, username = get_session_variables(self.request)
        print is_loggedin
        form.instance.created_by = User_info.objects.get(username=username)
        return super(ProposalCreateView, self).form_valid(form)