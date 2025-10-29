from django.shortcuts import render
from .forms import usersForm

def home(request):
    result = None
    form = usersForm()

    if request.method == "POST":
        form = usersForm(request.POST)
        if form.is_valid():
            n1 = form.cleaned_data['num1']
            n2 = form.cleaned_data['num2']

            # यहाँ पर हम दो नंबर जोड़ रहे हैं (string से int में convert करके)
            try:
                result = int(n1) + int(n2)
            except ValueError:
                result = "कृपया केवल नंबर दर्ज करें!"

    return render(request, 'home.html', {'form': form, 'result': result})
