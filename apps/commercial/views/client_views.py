from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from general.forms import CommentForm
from general.models import Client, Branch, Contact, Comment
from sales.forms.client_forms import ClientForm, ClientLookupForm, BranchForm, ContactForm
from sales.utils import obtener_datos_ruc

def clients_list(request):
    clients = Client.objects.all()
    form = ClientForm()
    return render(request, 'sales/client/clients_list.html', {'clients': clients, 'form': form})

def client_create(request):
    if request.method == "POST":
        form = ClientLookupForm(request.POST)
        ruc = request.POST.get("tax_id", "").strip()
        datos = obtener_datos_ruc(ruc)
        if datos:
            client, created = Client.objects.update_or_create(
                tax_id=ruc,
                defaults=datos
            )
            return redirect('client_detail', id=client.id)
    form = ClientLookupForm()
    return render(request, 'sales/client/partials/client_create_form.html', {'form': form})

def client_detail(request, id):
    client = get_object_or_404(Client, id=id)
    comment_form = CommentForm()
    content_type = ContentType.objects.get_for_model(Client)
    comentarios = Comment.objects.filter(content_type=content_type, object_id=client.id).order_by("-created_at")
    return render(request, 'sales/client/client_detail.html', {
        'client': client,
        'model_name': client._meta.model_name,
        'comment_form': comment_form,
        'comentarios': comentarios
    })

def client_edit(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', id=client.id)
    else:
        form = ClientForm(instance=client)
    return render(request, 'sales/client/partials/client_form.html', {'form': form, 'client': client})

def client_delete(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('clients_list')

# BRANCHS
def client_branch_create(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            new_branch = form.save(commit=False)
            new_branch.client = client
            new_branch.save()
            return render(request, 'sales/client/branch/branch_list.html', context={'client': client})
    else:
        form = BranchForm()
    return render(request, 'sales/client/branch/branch_form.html', {'form':form, 'client':client})

def client_branch_edit(request, id):
    branch = get_object_or_404(Branch, id=id)
    client = branch.client
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            print(f"Editado: {branch.name}")
            return render(request, 'sales/client/branch/branch_list.html', context={'client': client})
    else:
        form = BranchForm(instance=branch)
    return render(request, 'sales/client/branch/branch_edit.html', {'form':form, 'branch':branch, 'client':client})

def client_branch_delete(request, id):
    branch = get_object_or_404(Branch, id=id)
    client = branch.client
    if request.method == 'POST':
        branch.delete()
        return render(request, 'sales/client/branch/branch_list.html', context={'client': client})


# CONSULTANTS
def client_contact_create(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST, client=client)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.client = client
            new_contact.save()
            return render(request, 'sales/client/contact/contact_list.html', context={'client': client})
    else:
        form = ContactForm(client=client)

    return render(request, 'sales/client/contact/contact_form.html', {'form': form, 'client': client})

def client_contact_edit(request, id):
    contact = get_object_or_404(Contact, id=id)
    client = contact.client
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return render(request, 'sales/client/contact/contact_list.html', context={'client': client})
    else:
        form = ContactForm(instance=contact)
    return render(request, 'sales/client/contact/contact_edit.html', {'form': form, 'client': client, 'contact':contact})

def client_contact_delete(request, id):
    contact = get_object_or_404(Contact, id=id)
    client = contact.client
    if request.method == 'POST':
        contact.delete()
        return render(request, 'sales/client/contact/contact_list.html', context={'client': client})