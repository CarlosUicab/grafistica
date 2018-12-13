from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=({'class': 'form-control input-lg input-transparent',
                                                            'autofocus': 'autofocus',
                                                            'placeholder': ''})),
                             required=True, label="")
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False, attrs=({'class': 'form-control input-lg input-transparent',
                                                               'placeholder': ''})),
        required=True, label="")
    my_user = None  # Si se logea un usuario correctamente entonces se almacena aquí la sesión.

    def clean_password(self):
        """
        Verificamos si existen los datos que fueron enviados por el usuario.
        :return:
        """
        try:
            the_user = User.objects.get(email=self.cleaned_data['email'])
        except:
            the_user = None
        if the_user:
            if not the_user.is_active:
                raise forms.ValidationError(_("Cuenta no activada. ¿No ha recibido su correo de activación?"))
            user = authenticate(username=the_user.username,
                                password=self.cleaned_data['password'])
            if user is not None:
                self.my_user = user
            else:
                raise forms.ValidationError(_("Email y/o contraseña incorrecta"))
        else:
            raise forms.ValidationError(_("Email y/o contraseña incorrecta"))


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs=({'class': 'validate form-control',
                                                                'autofocus': 'autofocus'})),
                                 required=True, label=_("Nombre"))
    last_name = forms.CharField(widget=forms.TextInput(attrs=({'class': 'validate form-control'})),
                                required=True, label=_("Apellido(s)"))
    email = forms.EmailField(widget=forms.EmailInput(attrs=({'class': 'validate form-control', 'required': 'true',
                                                             'placeholder': _('yo@dominio.com')})),
                             required=True, label=_("Correo electrónico"))
    password_one = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                              attrs=({'class': 'validate form-control'})),
                                   required=True, label=_("Contraseña"))
    password_two = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                              attrs=({'class': 'validate form-control'})),
                                   required=True, label=_("Repita la contraseña"))

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError(_("Este email ya se encuentra registrado, ¿has perdido tu contraseña?"))
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_password_two(self):
        if self.cleaned_data['password_one'] == self.cleaned_data['password_two']:
            pass
        else:
            raise forms.ValidationError(_("Password no coincide, intente de nuevo"))