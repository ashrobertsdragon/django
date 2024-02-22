from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
  path("", views.landing_page, name="index"),  # Home/Landing page
  path('login/', views.CustomLoginView.as_view(), name='login'), # Login page
  path('signup/', views.signup_view,  name='signup'), # Sign up page

  path("account/", views.account_view, name="account"),  # Account management
  path("app/", views.lorebinder_form_view, name="lore_binder"),  # LoreBinders form page
  
  path("convert-ebook/", views.convert_ebook_view, name="convert_ebook"),  # Convert eBook page
  path("finetune/", views.finetune_view, name="finetune"),  # Fine-tune page
  path("fine-tune/instructions/", TemplateView.as_view(template_name="instructions.html"), name="fine_tune_instructions"), # Instructions for finetuning

  path("contact-us/", views.contact_form_view, name="contact_us"),  # Contact us page

  path("terms/", TemplateView.as_view(template_name="terms.html"), name="terms"), # TOS page
  path("privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"), # Privacy policy page
]
