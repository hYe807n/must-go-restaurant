from django.shortcuts import render, get_object_or_404
from first.models import Restaurant
from django.core.paginator import Paginator
from first.forms import RestaurantForm
from django.http import HttpResponseRedirect

# Create your views here.

def list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 5)
    lastpage = int(paginator.num_pages)-1
    page = request.GET.get('page')
    items = paginator.get_page(page)

    context={
        'restaurants' : items, 
        'lastPage' : lastpage,
    }

    return render(request, 'first/list.html', context)


def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/first/list/')
    form = RestaurantForm()
    return render(request, 'first/create.html', {'form' : form})


def update(request):
    if request.method == "POST" and 'id' in request.POST :
        #item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant, pk = request.POST.get('id'))
        form = RestaurantForm(request.POST, instance = item)
        if form.is_valid():
            item = form.save()
    elif request.method == "GET" :
        #item = Restaurant.objects.get(pk = request.GET.get('id'))
        item = get_object_or_404(Restaurant, pk = request.GET.get('id'))
        form = RestaurantForm(instance=item)
        return render(request, 'first/update.html', {'form' : form})
    return HttpResponseRedirect('/first/list/')


def detail(request):
    if 'id' in request.GET:
        item = get_object_or_404(Restaurant, pk = request.GET.get('id'))
        return render(request, 'first/detail.html', {'item' : item})
    return HttpResponseRedirect('/first/list/')


def delete(request):
    if 'id' in request.GET:
        item = get_object_or_404(Restaurant, pk = request.GET.get('id'))
        item.delete()
    return HttpResponseRedirect('/first/list/')