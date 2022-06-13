from django.shortcuts import render, get_object_or_404, redirect
from first.models import Restaurant, Review
from django.core.paginator import Paginator
from first.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg
from first.crawling.pages import crawling, mango, siksin, reset, dinning
import asyncio 


def list(request):
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point'))
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
        form = RestaurantForm(request.POST, request.FILES)
        form.photo = request.FILES['photo']
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/first/list/')
    form = RestaurantForm()
    return render(request, 'first/create.html', {'form' : form})


def update(request):
    if request.method == "POST" and 'id' in request.POST :
        #item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant, pk = request.POST.get('id'))
        password = request.POST.get('password', '')
        form = UpdateRestaurantForm(request.POST, instance = item)
        if form.is_valid() and password == item.password:
            item = form.save()
    elif request.method == "GET" :
        item = get_object_or_404(Restaurant, pk = request.GET.get('id'))
        form = RestaurantForm(instance=item)
        return render(request, 'first/update.html', {'form' : form})
    return HttpResponseRedirect('/first/list/')


def detail(request, id):
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'first/detail.html', {'item' : item, 'reviews' : reviews})
    return HttpResponseRedirect('/first/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk = id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('list')
        return redirect('restaurant-detail', id=id)
    return render(request, 'first/delete.html',{'item' : item})


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return redirect('restaurant-detail', id = restaurant_id)

    item = get_object_or_404(Restaurant, pk = restaurant_id)
    form = ReviewForm(initial={'restaurant' : item})
    return render(request, 'first/review_create.html', {'form' : form, 'item' : item})



def review_delete(request, restaurant_id, review_id):
    item =  get_object_or_404(Review, pk=review_id)
    item.delete()

    return redirect('restaurant-detail', id=restaurant_id)


def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)
    rlastpage = int(paginator.num_pages)-1

    page = request.GET.get('page')     #get 메서드로 page 번호를 받아온다
    items = paginator.get_page(page)    #해당 번호의 페이지를 items에 받는다

    context = {
        'reviews' : items,
        'rlastPage' : rlastpage,
    }
    return render(request, 'first/review_list.html', context)


async def search(request):
    if request.method=="GET":
        keyword = request.GET.get('search')
        reset()
        
        await asyncio.gather(mango(keyword), siksin(keyword), dinning(keyword))
        resobj = crawling()

        return render(request, 'first/search.html' ,{'searchlist': resobj})