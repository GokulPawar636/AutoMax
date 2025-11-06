from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm
from users.forms import LocationForm
from django.contrib import messages
from .filters import ListingFilter


def main_view(request):
    return render(request, 'main/main.html', {"name":"AutoMax"})  # ✅ include subfolder path

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset = listings)
    context = {
        "listing_filter": listing_filter,
    }
    return render(request, 'main/home.html',context)  # ✅ include subfolder path

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(
                    request, f'{listing.model} Listing Posted Successfully!')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'main/list.html', {'listing_form': listing_form, 'location_form': location_form, })

@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception('Listing Not Found')
        return render(request, 'main/listing.html', {'listing': listing},)  # ✅ include subfolder path
    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing.')
        return redirect('home')

@login_required
def edit_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    location_instance = listing.location if listing.location else None

    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES, instance=listing)
        location_form = LocationForm(request.POST, instance=location_instance)

        if listing_form.is_valid() and location_form.is_valid():
            try:
                listing_form.save()
                location_form.save()
                messages.success(request, f'{listing.model} Listing Updated Successfully!')
                return redirect('home')  # ✅ Redirect to home page
            except Exception as e:
                messages.error(request, 'An unexpected error occurred while saving the listing.')
                print(f"Save error: {e}")
                return redirect('home')  # ✅ Redirect even on error
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        listing_form = ListingForm(instance=listing)
        location_form = LocationForm(instance=location_instance)

    context = {
        'listing_form': listing_form,
        'location_form': location_form,
        'listing': listing,
    }
    return render(request, 'main/edit.html', context)
