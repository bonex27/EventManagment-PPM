from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView

from event.forms import EventForm
from event.models import Event


def set_message(request, message):
    """ Set a message in the session """
    request.session["message"] = message


def get_message(request):
    """ Get a message from the session """
    message = None
    if "message" in request.session:
        message = request.session["message"]
        del request.session["message"]
    return message if message else None


#List events
class EventListsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "avaevent"
        context["title"] = "Available Events"
        context["lists"] = Event.objects.exclude(participants=self.request.user.id)
        context["message"] = get_message(self.request)
        return context


class EventListsSubscribedView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "subevent"
        context["title"] = "Subscribed Events"
        context["lists"] = Event.objects.filter(participants=self.request.user.id)
        context["message"] = get_message(self.request)
        return context


class EventListsOrganizedView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "event/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "myevent"
        context["title"] = "My Events"
        context["lists"] = Event.objects.filter(owner=self.request.user.id)
        context["message"] = get_message(self.request)
        return context


class EventFormsCreate(LoginRequiredMixin, FormView):
    form_class = EventForm
    success_url = reverse_lazy("my-event-organized")
    template_name = "event/create_event.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        event = Event()
        if form.is_valid():
            event.owner = self.request.user
            event.name = form.cleaned_data["name"]
            event.description = form.cleaned_data["description"]
            event.date = form.cleaned_data["date"]
            event.save()

            event.participants.add(request.user)
            event.save()
            set_message(request, f"Created event {event.name}")
            return redirect("my-event-organized")
        else:
            return self.form_invalid(form)


class EventDetailView(LoginRequiredMixin, View):
    template = "event/event-detail.html"

    def get(self, request, event_id):
        # if request.user not in Event.objects.get(id=event_id).participants.all():
        #     #set_message(request, "You are not a participant of this list.")
        #     return redirect("lists")

        event = Event.objects.get(id=event_id)
        return render(request, self.template, {"event": event})


class EditEventView(LoginRequiredMixin, FormView):
    form_class = EventForm
    success_url = reverse_lazy("my-event-organized")
    template_name = "event/edit_event.html"
    context = {

    }

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=self.kwargs["event_id"])
        form = self.form_class()
        self.context['form'] = form

        return render(request, self.template_name, self.context)

    # def get(self, request, *args, **kwargs):
    #     event = Event.objects.get(pk=self.kwargs["pk"])
    #     if event.owner != self.request.user:
    #         return redirect("")
    #     return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs["pk"])
        if event.owner != self.request.user:
            return redirect("")
        set_message(request, f"Edited event {event.name}")
        return super().post(request, *args, **kwargs)


class EventDeleteView(LoginRequiredMixin, View):
    model = Event

    def get(self, request, *args, **kwargs):
        # Only the task list participants can comment
        if request.user != Event.objects.get(id=kwargs.get("user")).owner:
            #set_message(request, "You are not a participant of this list.")
            return redirect("my-event-organized")

        event = Event.objects.get(id=kwargs.get("pk"))
        event.delete()
        set_message(request, f"Deleted event {event.name}")
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
        set_message(request, f"Subscribed event {event.name}")
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
            set_message(request, f"Unsubscribed from {event.name}")
            return redirect("my-event-subscribe")
        else:
            set_message(request, f"You can't unscribe from your events")
            return redirect("my-event-subscribe")


class EventRemoveUserView(LoginRequiredMixin, View):
    model = Event

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get("user"))
        # Only the task list participants can comment
        if user in Event.objects.get(
                id=kwargs.get("event")).participants.all():
            if request.user == Event.objects.get(
                    id=kwargs.get("event")).owner:
                event = Event.objects.get(id=kwargs.get("event"))
                event.participants.remove(user.id)
                event.save()
                set_message(request, f"{user.username} removed from {event.name}")
                return redirect("event_details",event_id=kwargs.get("event"))
            else:
                set_message(request, f"Cannot remove user from not owned event")
        else:
            set_message(request, f"Cannot remove user from not subscribed event")
        return redirect("event_details",event_id=kwargs.get("event"))
