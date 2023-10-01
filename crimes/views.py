from django.shortcuts import render
from .forms import CreateCrimeForm
# Create your views here.
def create_crime(request):
    if request.method == 'POST':
        form = CreateCrimeForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = CreateCrimeForm()

    context = {
        'form': form
    }
    return render(request, 'crimes/create_crime.html', context)