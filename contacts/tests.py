from django.test import TestCase
from contacts.models import Contact
from django.test.client import Client
from django.test.client import RequestFactory
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from rebar.testing import flatten_to_dict
from contacts import forms
import django.http
import django.utils.unittest as unittest2

# Create your tests here.

class ContactTests(TestCase):
    """Contact model tests."""

    def test_str(self):

        contact = Contact(first_name='John', last_name='Smith')

        self.assertEquals(
            str(contact),
            'John Smith',
        )
class ContactListViewTests(TestCase):
    """Contact list view tests."""

    def test_contacts_in_the_context(self):

        client = Client()
        response = client.get('/')

        self.assertEquals(list(response.context['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = ListContactView.as_view()(request)

        self.assertEquals(list(response.context_data['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')
        response = ListContactView.as_view()(request)
        self.assertEquals(response.context_data['object_list'].count(), 1)

class ContactListIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ContactListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactListIntegrationTests, cls).tearDownClass()

    def test_contact_listed(self):

        # create a test contact
        Contact.objects.create(first_name='foo', last_name='bar')

        # make sure it's listed as <first> <last> on the list
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[0].text,
            'foo bar'
        )

    def test_add_contact_linked(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
            self.selenium.find_element_by_link_text('add contact')
        )

    def test_add_contact(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@example.com')

        self.selenium.find_element_by_id("save_contact").click()
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[-1].text,
            'test contact'
        )

class EditContactFormTests(TestCase): #Then we can write a unit test that tests two cases: success (email addresses match) and failure (they do not).

    def test_mismatch_email_is_invalid(self):

        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'bar@example.com'

        bound_form = forms.ContactForm(data=form_data)
        self.assertFalse(bound_form.is_valid())

    def test_same_email_is_valid(self):

        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'foo@example.com'

        bound_form = forms.ContactForm(data=form_data)
        self.assert_(bound_form.is_valid())

