from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from formulairmail.email import mail
from formulairmail.forms import Email_form
from formulairmail.models import Email
from library_gn import settings
from reader.models import *


# Create your views here.
@login_required(login_url='login')
def vuemail(request):
    form = mail()
    if request.user.is_superuser:
        R = Reader.objects.exclude(status=0).exclude(type_Reader = 1)
    else:
        R = Reader.objects.exclude(status=0).filter(readpoint = request.user.readpoint).exclude(type_Reader = 1)

    listmail = []
    for l in R:
        a = {
            'email': l.email
        }
        listmail.append(a)
    return render(request, 'formulairmail/index.html', {'form': form, 'listmail': listmail, 'r': R})


def email(request):
    if request.method == 'POST':
        form = Email_form(request.POST)
        emailDestinateur = request.POST['email_exp']
        emailDestinateur = emailDestinateur.split(",")
        message = request.POST['message']
        obj = request.POST['object']
        if form.is_valid():
                try:
                    if send_mail(subject=obj, message=message, from_email=settings.EMAIL_HOST_USER,
                                 recipient_list=[emailDestinateur],
                                 fail_silently=False, html_message=message):
                        form.save()
                        messages.success(request, "Evoi effectué avec succès")
                        return redirect('formulairmail/index.html')
                    else:
                        messages.error(request, "Erreur d'envoi")
                        return ('mail')

                except:
                    messages.error(request, f"impossible d  'envoyer veuillez ressayer.")
                    return redirect('mail')

        else:
            messages.error(request, "Erreur d'envoi")
            em = Email.objects.filter(status = 1).exclude(status=0)
            context = {
                'tooltip': 'Envoi de mail',
                'form': form,
                'email': em
            }
            return render(request, 'mail', context)
    else:
        form = Email_form()
        em = Email.objects.filter(status = 1).exclude(status=0)
        R = Reader.objects.exclude(status=0)
        i = 1
        listmail = []
        for l in R:
            a = {
                'num': i,
                'email': l.email
            }
            listmail.append(l.email)
            i += 1
        return render(request, 'formulairmail/index.html', {'form': form, 'listmail': listmail, 'r': R, 'email': em})
