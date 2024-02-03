from django.shortcuts import render
from django.contrib.auth import logout
def home(request):

    context = {
        'user': request.user,
    }

    return render(request, 'clinic/home.html', context)

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                f'Contact Form Submission: {subject}',
                f'Name: {name}\nEmail: {email}\n\n{message}',
                'your_email@example.com',  
                ['your_email@example.com'],  
                fail_silently=False,
            )

            return render(request, 'success.html')  
    else:
        form = ContactForm()

    return render(request, 'clinic/contact.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('clinic:home')
