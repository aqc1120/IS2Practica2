from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from .models import Opinion, Cruise
from .forms import OpinionForm
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    # Ordena los destinos según la popularidad
    all_destinations = models.Destination.objects.all().order_by('-popularity')  # Asegúrate de tener el campo `popularity`
    
    # Toma los tres primeros destinos más populares
    top_destinations = all_destinations[:3]

    # El resto de los destinos
    other_destinations = all_destinations[3:]

    return render(request, 'destinations.html', {
        'top_destinations': top_destinations,
        'other_destinations': other_destinations,
    })
def opinion(request):
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            # Guardar la opinión en la base de datos
            Opinion.objects.create(
                name=form.cleaned_data['name'],
                cruise=form.cleaned_data['cruise'],
                opinion=form.cleaned_data['opinion'],
                valoracion=form.cleaned_data['valoracion']
            )
            # Redirigir a la misma página después de enviar la opinión
            return redirect('opinion')
    else:
        form = OpinionForm()
    opinions = Opinion.objects.all()
    cruises = Cruise.objects.all()
    return render(request, 'opinion.html', {'form': form, 'opinions': opinions, 'cruises': cruises})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class DestinationCreateView(generic.CreateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description']

class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description']

class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    fields = ('destinations')

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

   # Sobrescribir form_valid para enviar el correo
    def form_valid(self, form):
        # Obtiene los datos del formulario
        response = super().form_valid(form)
        info_request = form.instance
        
        # Envía el correo
        send_mail(
            subject='Info Request Received',
            message=f"Hello {info_request.name},\n\nWe have received your request for more information about the cruise '{info_request.cruise}'. We will get back to you soon!\n\nThank you for reaching out!",
            from_email='your_email@example.com',  # Cambia por tu correo configurado
            recipient_list=[info_request.email],  # Correo del usuario
        )
        
        return response