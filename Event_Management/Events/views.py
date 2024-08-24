from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Event,Registration
from django.contrib import messages
from .forms import RegistrationForm

def event_list(request):
    query = request.GET.get('q')
    if query:
         events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = Registration.objects.filter(event=event, user=request.user).first()
    return render(request, 'events/event_details.html', {'event': event, 'registration': registration,})


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


@login_required
def unregister_from_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = Registration.objects.filter(event=event, user=request.user).first()
    if registration:
        registration.delete()
        messages.success(request, f'You have successfully unregistered from {event.title}.')
    else:
        messages.error(request, f'You are not registered for {event.title}.')
    return redirect('event_detail', pk=event.pk)



@login_required
def user_dashboard(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'events/user_dashboard.html', {'registrations': registrations})
