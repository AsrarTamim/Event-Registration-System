from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Event,Registration
from django.contrib import messages
from .forms import RegistrationForm
from django.utils import timezone

def event_list(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(date__gt=now.date()) | Event.objects.filter(date=now.date(), time__gte=now.time())
    finished_events = Event.objects.filter(date__lt=now.date()) | Event.objects.filter(date=now.date(), time__lt=now.time())
    query = request.GET.get('q')
    if query:
        upcoming_events = upcoming_events.filter(title__icontains=query)
        finished_events = finished_events.filter(title__icontains=query)
    return render(request, 'events/event_list.html', {
        'upcoming_events': upcoming_events.order_by('date', 'time'),
        'finished_events': finished_events.order_by('-date', '-time')
        })

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    now = timezone.now()
    is_upcoming = (event.date > now.date()) or (event.date == now.date() and event.time >= now.time())
    registration = Registration.objects.filter(event=event, user=request.user).first()
    return render(request, 'events/event_details.html', {
        'event': event, 
        'registration': registration,
        'is_upcoming': is_upcoming
        })


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.slots > 0:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                registration = form.save(commit=False)
                registration.event = event
                registration.user = request.user
                registration.save()
                event.slots -= 1
                event.save()                
                messages.success(request, 'You have successfully registered for the event!')
                return redirect('event_detail', pk=event.pk)
        else:
            form = RegistrationForm()
    else:
        messages.error(request, 'Sorry, no slots are available for this event.')
        return redirect('event_detail', pk=event.pk)
    return render(request, 'events/event_register.html', {'event': event, 'form': form})


@login_required
def unregister_from_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = Registration.objects.filter(event=event, user=request.user).first()
    if registration:
        registration.delete()
        event.slots += 1
        event.save()
        messages.success(request, f'You have successfully unregistered from {event.title}.')
    else:
        messages.error(request, f'You are not registered for {event.title}.')
    return redirect('event_detail', pk=event.pk)



@login_required
def user_dashboard(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'events/user_dashboard.html', {'registrations': registrations})
