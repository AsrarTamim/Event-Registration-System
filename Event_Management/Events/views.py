from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Event,Registration
from django.contrib import messages
from .forms import RegistrationForm

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_details.html', {'event': event})


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, 'You have successfully registered for the event!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = RegistrationForm()

    return render(request, 'events/event_register.html', {'event': event, 'form': form})