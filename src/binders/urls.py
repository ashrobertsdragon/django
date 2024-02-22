from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
  path("", views.landing_page, name="index"),  # Home/Landing page
  path("account/", views.account, name="account"),  # Account management
  path("app/", views.lorebinder_form, name="lore_binder"),  # LoreBinders form page
  
  path("convert-ebook/", views.convert_ebook, name="convert_ebook"),  # Convert eBook page
  path("finetune/", views.finetune, name="finetune"),  # Fine-tune page
  path("fine-tune/instructions/", TemplateView.as_view(template_name="instructions.html"), name="fine_tune_instructions"),

  path("terms/", TemplateView.as_view(template_name="terms.html"), name="terms"),
  path("privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
]
