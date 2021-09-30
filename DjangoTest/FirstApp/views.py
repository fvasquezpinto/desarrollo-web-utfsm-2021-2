import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Animals
 
def index(request):
    """Primera "function view" de la app demo.

    Define un contexto y hace render de un template.
    """
    context = {"my_var": "Hola!"}
    return render(
        request,
        "extended_tem.html",
        context,
    )

def create_cat(request):
    """Function view en que se utiliza el ORM de Django para crear un objecto"""
    name = "Cat"
    weight = 4
    Animals.objects.create(name=name, weight=weight)
    context = {"name": name, "weight": weight}
    return render(
        request,
        "create_animal.html",
        context,
    )

def create_animal(request, name, weight):
    Animals.objects.create(name=name, weight=weight)
    context = {"name": name, "weight": weight}
    return render(
        request,
        "create_animal.html",
        context,
    )

def review_animals(request):
    "Function view en la que obtenemos todos los objetos de un modelo"
    animals = Animals.objects.all()
    context = {"animals": animals}
    return render(
        request,
        "review_animals.html",
        context,
    )


class AnimalsListView(generic.ListView):
    """Class based view. Se recomienda implementar este tipo de vistas.

    Nota: ver que en urls.py se carga ligeramente diferente a las function views
    Nota 2: no siempre se usa generic.ListView, ya que esta requiere pasarle un modelo.
    Se puede usar simplemente View (from django.views import View), ver más en
    https://docs.djangoproject.com/en/3.2/topics/class-based-views/intro/#using-class-based-views
    """
    model = Animals
    # el nombre que tendrá en el template la variable con los datos del modelo
    context_object_name = "animals_list"
    # template que queremos que la vista cargue
    template_name = "animals_list.html"

    # esto lo hacemos solo para poder hacer un request de tipo POST a esta vista
    # desde afuera de nuestra app (otra máquina, otra plataforma como Postman, etc)
    # si no necesitamos disponibilizar el método POST o las solicitudes solo vendrán
    # desde esta app, entonces no es necesario definir las siguientes tres líneas
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AnimalsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # especificamos qué es lo que tendrá en el template la variable animals_list
        return Animals.objects.all().order_by("-weight")[:3]
    
    def get_context_data(self, **kwargs):
        """Crear el context que recibirá el template"""
        # cargar contexto de implementación base
        context = super(AnimalsListView, self).get_context_data(**kwargs)
        # cargar data al context
        context["my_var"] = "Esto lo paso al template como context data"
        context["my_var2"] = 14
        return context
    
    def post(self, request, *args, **kwargs):
        """Disponibilizamos el método POST para esta vista

        Nota: podríamos consultar esta vista desde Postman
        """
        animals = Animals.objects.all().order_by("-weight")[:3]
        animals_list = []
        for animal in animals:
            animals_list.append(
                {"id": animal.id, "name": animal.name, "weight": animal.weight}
            )
        
        # convertimos la data a JSON, puesto que este es el tipo de dato que podemos
        # enviar en una respuesta HTTP (de lo contrario podría fallar)
        json_with_the_data = json.dumps(animals_list)
        return HttpResponse(
            content=json_with_the_data, content_type="application/json"
        )
