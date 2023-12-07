from django.shortcuts import render


def main(request):
    url_name = 'main'
    return render(request, 'catalog/main.html', {'url_name': url_name})


def contact_info(request):
    url_name = 'contact_info'
    return render(request, 'catalog/contact_info.html', {'url_name': url_name})


def contact_form(request):
    url_name = 'contact_form'
    sent = False
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(name, email)
        sent = True

    return render(request, 'catalog/contact_form.html', {'url_name': url_name, 'sent': sent})
