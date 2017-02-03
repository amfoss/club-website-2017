from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from fossWebsite.helper import get_session_variables
from .models import Proposal
from register.models import User_info

# Create your views here.

class ProposalListView(ListView):
    model = Proposal

    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = Proposal.objects.all()
        context = self.get_context_data(object_list=self.object_list)
        is_loggedin, username = get_session_variables(self.request)
        if is_loggedin is False:
            return redirect('login')
        return self.render_to_response(context)


class ProposalCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = Proposal.objects.all()
        context = self.get_context_data(object_list=self.object_list)
        is_loggedin, username = get_session_variables(self.request)
        if is_loggedin is False:
            return redirect('login')
        return self.render_to_response(context)

    model = Proposal
    fields = '__all__'

    def form_valid(self, form):
        is_loggedin, username = get_session_variables(self.request)
        print is_loggedin
        form.instance.created_by = User_info.objects.get(username=username)
        return super(ProposalCreateView, self).form_valid(form)


class ProposalUpdateView(UpdateView):

    model = Proposal

    fields = '__all__'

    template_name = 'fossProposal/proposal_form.html'