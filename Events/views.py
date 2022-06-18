from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Events.forms import EventsFrom
from Events.models import Events
from rest_framework import viewsets
from Events.serialiser import api_event


# Create your views here.
def events(request):
    if request.method == 'POST':
        formulaire = EventsFrom(request.POST, request.FILES)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Ajoute avec success')
            return redirect('event')
        else:
            messages.error(request, 'erreur')
            return redirect('event')
    formulaire = EventsFrom()
    listes = Events.objects.filter(status=1)
    context = {
        'form': formulaire,
        'titre': 'Ajout d\'un Evenements',
        'listes': listes
    }
    return render(request, 'events/events.html', {'context': context})


def list_events(request):
    listes = Events.objects.filter(status=1)
    context = {
        'tooltip': 'Liste des Evenements',
        'listes': listes
    }
    return render(request, 'events/list_events.html', {'context': context})


def delete(request, id):
    event = Events.objects.get(pk=id)
    event.status = 0
    event.save()
    return redirect('event')


def edit(request, id):
    event = Events.objects.get(pk=id)
    if request.method == 'POST':
        form = EventsFrom(request.POST, request.FILES, instance=event)
        form.save()
        return redirect('event')
    else:
        eventform = EventsFrom(instance=event)
        context = {
            'form': eventform,
            'titre': 'Modification Evennement'
        }
        return render(request, 'events/edit_events.html', {'context': context})


def detail_event(request, id):
    event = Events.objects.get(pk=id)
    context = {
        'event': event,
        'titre': 'Detail Evennement'
    }
    return render(request, 'events/detail_event.html', {'context': context})


class viewapievent(viewsets.ModelViewSet):
    queryset = Events.objects.filter(status=1)
    serializer_class = api_event


# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        events = Events.objects.filter(status=1)
        # changer le chemin du temble
        pdf = html_to_pdf('Events/printEvents.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "events": events,
            # le tooltip
            "title":'Liste Des événéments'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')
    #PPRES TOUS ON CREE L'UREL POUR CETTE VIEW
