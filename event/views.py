from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from event.models import Event


#List events
class EventListsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "avaevent"
        context["title"] = "Available Events"
        context["lists"] = Event.objects.exclude(participants=self.request.user.id)
        context["message"] = "hello"
        return context


class EventListsSubscribedView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "subevent"
        context["title"] = "Subscribed Events"
        context["lists"] = Event.objects.filter(participants=self.request.user.id)
        context["message"] = "hello"
        return context


class EventListsOrganizedView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "myevent"
        context["title"] = "My Events"
        context["lists"] = Event.objects.filter(owner=self.request.user.id)
        context["message"] = "hello"
        return context


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ["name", "date", "description"]

    template_name = "event/create_event.html"
    success_url = reverse_lazy("lists")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.owner = self.request.user

            task_list = form.save()

            # Add the user as owner and participant
            task_list.participants.add(self.request.user)
            task_list.save()
            return redirect("event-list")
        else:
            return self.form_invalid(form)


class EventDeleteView(LoginRequiredMixin, View):
    model = Event

    def get(self, request, *args, **kwargs):
        # Only the task list participants can comment
        if request.user != Event.objects.get(id=kwargs.get("pk")).owner:
            #set_message(request, "You are not a participant of this list.")
            return redirect("my-event-organized")

        event = Event.objects.get(id=kwargs.get("pk"))
        event.delete()
        return redirect("my-event-organized")


class EventSubscribeView(LoginRequiredMixin, View):
    model = Event

    def get(self, request, *args, **kwargs):
        # Only the task list participants can comment
        if request.user in Event.objects.get(id=kwargs.get("pk")).participants.all():
            #set_message(request, "You are not a participant of this list.")
            return redirect("event-list")

        event = Event.objects.get(id=kwargs.get("pk"))
        event.participants.add(request.user)
        event.save()
        return redirect("event-list")


class EventUnscribeView(LoginRequiredMixin, View):
    model = Event

    def get(self, request, *args, **kwargs):
        # Only the task list participants can comment
        if request.user in Event.objects.get(
                id=kwargs.get("pk")).participants.all() and not request.user == Event.objects.get(
                id=kwargs.get("pk")).owner:

            event = Event.objects.get(id=kwargs.get("pk"))
            event.participants.remove(self.request.user)
            event.save()
            return redirect("my-event-subscribe")
        else:
            return redirect("my-event-subscribe")
