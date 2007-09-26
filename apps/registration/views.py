from django.core import formfields, validators
from django.core.extensions import DjangoContext, render_to_response
from django.core.template import loader, Context
from django.core.validators import ValidationError
from django.models.auth import users
from django.models.core import sites
from django.parts.auth.formfields import AuthenticationForm
from django.utils.httpwrappers import HttpResponse, HttpResponseRedirect
from django.views.decorators.auth import login_required
from django.views.auth.login import login

REDIRECT_FIELD_NAME = 'next'

class RegistrationManipulator(AuthenticationForm):
    # we inherit a few useful methods
    def __init__(self, request):
        AuthenticationForm.__init__(self, request)
        self.fields = (
            formfields.TextField(field_name="username", is_required=True,
                                 length=15, maxlength=30,
                                 validator_list=[self.isValidUsername, self.hasCookiesEnabled]),
            formfields.PasswordField(field_name="password",
                                     is_required=True,
                                     length=15, maxlength=30,
                                     validator_list=[self.isOkPassword]),
            formfields.PasswordField(field_name="password2", is_required=True,
                                     length=15, maxlength=30,
                                     validator_list=[validators.AlwaysMatchesOtherField('password2', "The two 'new password' fields didn't match.")]),
            formfields.EmailField(field_name="email", is_required=True),
                      )
    def isValidUsername(self, field_data, all_data):
        if not field_data.isalnum():
            raise ValidationError("Usernames can only consist of letters, digits, and _'s")
        try:
            users.get_object(username__exact=field_data)
        except users.UserDoesNotExist:
            pass
        else:
            raise ValidationError("That username is already taken.  Please choose another.")
        if len(field_data) < 2:
            raise ValidationError("Usernames must be at least two characters long")

    def isOkPassword(self, field_data, all_data):
        if len(field_data) < 3:
            raise ValidationError("Passwords must be at least three characters long")
    def save(self, data):
        from django.core.mail import send_mail
        from django.models.core import sites
        username = data['username']
        password = data['password']
        email = data['email']
        u = users.create_user(username, email, password)
        u.save()
        current_site = sites.get_current()
        site_name = current_site.name
        domain = current_site.domain
        t = loader.get_template('registration/account_creation_email')
        c = {
            'username': username,
            'password': password,
            'email': email,
            'domain': domain,
            'site_name': site_name,
        }
        #send_mail('Account created on %s' % site_name, t.render(Context(c)), None, [email])


def register(request):
    from django.models.core import sites
    "Displays the registration form and handles the registration action"
    manipulator = RegistrationManipulator(request)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if request.POST:
        errors = manipulator.get_validation_errors(request.POST)
        if not errors:
            data = request.POST.copy()
            manipulator.save(data)
            login(request)
            return HttpResponseRedirect('/')
    else:
        errors = {}
    request.session.set_test_cookie()
    return render_to_response('registration/register' ,{
        'form': formfields.FormWrapper(manipulator, request.POST, errors),
        REDIRECT_FIELD_NAME: redirect_to,
        'site_name': sites.get_current().name,
    }, context_instance=DjangoContext(request))



