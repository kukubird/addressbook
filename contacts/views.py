from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from django.views.generic import ListView
from contacts.models import Contact
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.views.generic import DeleteView
from django.views.generic import DetailView
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, World")

class LoggedInMixin(object): # class mixin that ensures the user is logged in

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class MyView(View): #class based views

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World")

class ListContactView(LoggedInMixin, ListView): #a view that presents a list of contacts in the database

    model = Contact
    template_name = 'contact_list.html'

    def get_queryset(self):

        return Contact.objects.filter(owner=self.request.user)

class CreateContactView(CreateView): #a view for adding a new contact

    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):

        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')

        return context

class UpdateContactView(UpdateView): #view for editing contacts

    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):

        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',
                                    kwargs={'pk': self.get_object().id})

        return context

class DeleteContactView(DeleteView): #view for deleting contact

    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')

class ContactView(DetailView): # view for details for our contacts, this will show the details of the contacts

    model = Contact
    template_name = 'contact.html'

class EditContactAddressView(UpdateView): #view for edit addresses html

    model = Contact
    template_name = 'edit_addresses.html'
    form_class = forms.ContactAddressFormSet

    def get_success_url(self):

        # redirect to the Contact view.
        return self.get_object().get_absolute_url()

