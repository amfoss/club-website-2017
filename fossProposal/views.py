from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from fossWebsite.helper import get_session_variables
from .models import Proposal
from register.models import User_info


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


class ProposalDetailView(DetailView):

    model = Proposal

    def get_context_data(self, **kwargs):
        context = super(ProposalDetailView, self).get_context_data(**kwargs)
        is_loggedin, username = get_session_variables(self.request)
        if is_loggedin is False:
            return redirect('login')
        return context


class ProposalCreateView(CreateView):

    model = Proposal
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = Proposal.objects.all()
        context = self.get_context_data(object_list=self.object_list)
        is_loggedin, username = get_session_variables(self.request)
        if is_loggedin is False:
            return redirect('login')
        return self.render_to_response(context)

    def form_valid(self, form):
        is_loggedin, username = get_session_variables(self.request)
        form.instance.created_by = User_info.objects.get(username=username)
        return super(ProposalCreateView, self).form_valid(form)


class ProposalUpdateView(UpdateView):

    model = Proposal
    fields = '__all__'
    template_name = 'fossProposal/proposal_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProposalUpdateView, self).get_context_data(**kwargs)
        is_loggedin, username = get_session_variables(self.request)
        if is_loggedin is False:
            return redirect('login')
        return context
