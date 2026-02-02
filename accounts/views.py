from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login
from .form import SignUpForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/profile')
            # You can authenticate and login the user here if needed
            # You can add a redirect to login page or home page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})