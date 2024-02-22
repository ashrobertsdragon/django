from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class SignupForm(UserCreationForm):
  email = forms.EmailField(
    required=True,
    help_text="Required. Add a valid email address.",
    widget=forms.EmailInput(attrs={"aria-label": "Email address"})
  )
  name = forms.CharField(
    max_length=30,
    required=True,
    help_text='Required.',
    widget=forms.TextInput(attrs={"aria-label": "Name"})
  )
  birthdate = forms.DateField(
    label="Birthdate",
    required=True,
    help_text='Required for COPPA compliance.',
    widget=forms.DateInput(attrs={"type": "date"}),
  )
  password = forms.CharField(
    max_length=30,
    label="Password",
    required=True,
    help_text='Required.',
    widget=forms.PasswordInput(attrs={"aria-label": "Password"})
  )

  class Meta:
    model = User
    fields = ("email", "password", "name", "birthdate")

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(username=email).exists():
      raise ValidationError("A user with that email already exists.")
    return email

  def save(self, commit=True):
    user = super(SignupForm, self).save(commit=False)
    user.username = self.cleaned_data['email']  # Use email as username
    user.set_password(self.cleaned_data['password'])
    user.first_name = self.cleaned_data.get('name', '').split(' ')[0]
    user.last_name = ' '.join(self.cleaned_data.get('name', '').split(' ')[1:])
    if commit:
      user.save()
    return user
class CustomLoginForm(AuthenticationForm):
  username = forms.EmailField(
    label="Email address",
    required=True,
    help_text="Required. Add a valid email address.",
    widget=forms.EmailInput(attrs={"aria-label": "Email address", "autofocus": True})
  )
  password = forms.CharField(
    label="Password",
    required=True,
    help_text="Required.",
    widget=forms.PasswordInput(attrs={"aria-label": "Password"})
  )

  def confirm_login_allowed(self, user):
    super().confirm_login_allowed(user)

class AccountManagementForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["name", "birthdate", "email",]

class LoreBinderForm(forms.Form):
  author_name = forms.CharField(
    max_length=30, 
    widget=forms.TextInput(attrs={"aria-label": "Author name for manuscript"})
  )
  book_title = forms.CharField(
    max_length=50,
    widget=forms.TextInput(attrs={"aria-label": "Book title"})
  )
  is_first_person = forms.BooleanField(
    required=False,
    label="First Person Narrative",
    widget=forms.CheckboxInput(attrs={"aria-label": "Choose first or third person for manuscript"})
  )  # 1st/3rd person toggle
  narrator_name = forms.CharField(
    max_length=30,
    required=False,
    widget=forms.TextInput(attrs={"aria-label": "Narrator's name"})
  )  # Conditional, shown only for 1st person

  # Visible fields for user input; these will be handled by JavaScript
  character_attributes_input = forms.CharField(
    label="Character Attributes",
    widget=forms.TextInput(
      attrs={"autocomplete": "off", "aria-label": "Character attributes to include"}
    ),
    required=False
  )
  other_attributes_input = forms.CharField(
    label="Other Attributes",
    widget=forms.TextInput(
      attrs={"autocomplete": "off", "aria-label": "Other attributes for AI to search for"}
    ),
    required=False
    )

  # Hidden fields to store the comma-separated values
  character_attributes = forms.CharField(widget=forms.HiddenInput(), required=False)
  other_attributes = forms.CharField(widget=forms.HiddenInput(), required=False)

  file_upload = forms.FileField(
    widget=forms.ClearableFileInput(
      attrs={"multiple": False,
            "accept": "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/epub+zip, application/pdf, text/plain"}
    ),
    required=True
  )

class ContactForm(forms.Form):
  name = forms.CharField(widget=forms.TextInput(
    attrs={"aria-label": "Your name", "aria-required": "true"})
    )
  email = forms.EmailField(widget=forms.EmailInput(
    attrs={"aria-label": "Your email address", "aria-required": "true"})
    )
  message = forms.CharField(widget=forms.Textarea(
    attrs={"aria-label": "Your message", "rows": "5"}
    ))

class MultipleFileInput(forms.ClearableFileInput):
  allow_multiple_selected = True

class MultipleFileField(forms.FileField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("widget", MultipleFileInput())
    super().__init__(*args, **kwargs)

  def clean(self, data, initial=None):
    single_file_clean = super().clean
    if isinstance(data, (list, tuple)):
      result = [single_file_clean(d, initial) for d in data]
    else:
      result = single_file_clean(data, initial)
    return result

class FineTuneForm(forms.Form):
  user_key = forms.CharField(
    max_length=60,
    widget=forms.PasswordInput,
    required=True
  )
  file = MultipleFileField(
    widget=MultipleFileInput(attrs={"multiple": True, "accept": "text/plain"}),
    required=True
  )
  role = forms.CharField(widget=forms.Textarea, required=True)
  chunk_type = forms.ChoiceField(
    choices=[
      ("sliding_window_small", "Sliding Window (chapter-level)"),
      ("sliding_window_large", "Sliding Window (book-level)"),
      ("dialogue_prose", "Dialogue/Prose"),
      ("generate_beats", "Generate Beats (extra cost)")
    ],
    required=True
  )
  rights_confirmation = forms.BooleanField(required=True)
  terms_agreement = forms.BooleanField(required=True)

class ConvertEbookForm(forms.Form):
  book_title = forms.CharField(
    max_length=50,
    widget=forms.TextInput(
      attrs={"aria-label": "Book title"}
    )
  )
  author_name = forms.CharField(
    max_length=30,
    widget=forms.TextInput(
      attrs={"aria-label": "Author name for manuscript"}
    )
  )
  file = forms.FileField(
    widget=forms.ClearableFileInput(
      attrs={"multiple": False, "accept": "application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/epub+zip, application/pdf, text/plain"}
    ),
    required=True
  )
  rights_confirmation = forms.BooleanField(required=True)
  terms_agreement = forms.BooleanField(required=True)