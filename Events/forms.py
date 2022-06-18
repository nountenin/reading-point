from django import  forms
from Events.models import Events

class EventsFrom(forms.ModelForm):
    class Meta:
        model = Events
        fields = [
            'title_events','descriptions','image_events','type'
        ]
        labels = {
            'title_events': " Titre de l'evennement ",
            'descriptions': " Descriptions ",
            'image_events': "Image de l'evennement" ,
            'type' : "Type de l'evennement"
        }