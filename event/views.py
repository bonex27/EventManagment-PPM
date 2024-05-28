from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from event.models import Event


#List events
class EventListsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lists"] = Event.objects.filter(participants=self.request.user.id)
        context["message"] = "hello"
        return context