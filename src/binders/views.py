import logging
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from django.core.files.storage import default_storage


#import stripe

from binders.forms import AccountManagementForm, LoreBinderForm, ContactForm, FineTuneForm, ConvertEbookForm
from binders.models import BindersTable
from binders.utils import process_lorebinder, check_pdf_in_storage, contact, random_str, is_encoding
from binders.logging_config import start_loggers


start_loggers()
error_logger = logging.getLogger("error_logger")

def landing_page(request):
  return render(request, "index.html")

@login_required
def lorebinder_form(request):
  if request.method == "POST":
    form = LoreBinderForm(request.POST, request.FILES)
    if form.is_valid():
      process_lorebinder(form.cleaned_data, request.user)
      return JsonResponse({"success": True, "message": "Your submission is being processed. Expect an email within an hour."})
    else:
      form = LoreBinderForm()

  return render(request, "lorebinder.html", {"form": form})

@login_required
def account(request):
  section = request.GET.get("section", "profile")  # Default to "profile" section

  if section == "loreprosebinders":
      return view_loreprosebinders(request)
  elif section == "profile":
      return profile(request)
  elif section == "buy_credits":
      return buy_credits(request)
  else:
      return redirect("account") 

def profile(request):
  message = ""
  if request.method == "POST":
    form = AccountManagementForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      message = "Your account has been updated successfully."  # Set success message
    else:
      message = "There was an error updating your account."  # Set error message if form is not valid
  else:
    form = AccountManagementForm(instance=request.user)

  return render(request, "account_management.html", {"form": form, "message": message})

def view_loreprosebinders(request):
  loreprosebinders = BindersTable.objects.filter(user=request.user)
  lorebinder_data = []

  for lorebinder in loreprosebinders:
    pdf_path = f"{request.user.folder_name}/{lorebinder.book_title}/lorebinder-{lorebinder.book_title}.pdf"
    pdf_exists = check_pdf_in_storage(pdf_path)

    lorebinder_data.append({
      "lorebinder": lorebinder,
      "pdf_exists": pdf_exists,
      "pdf_path": pdf_path if pdf_exists else None
    })

  return render(request, "loreprosebinders_list.html", {"loreprosebinders": lorebinder_data})

def buy_credits(request):
  pass

def contact_form(request):
  form = ContactForm()
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data.get('name')
      email = form.cleaned_data.get('email')
      message = form.cleaned_data.get('message')
      contact(email, name, message)
  return render(request, "contact-us.html", {"form":form})

def finetune(request):
  min_size = 1024 # 1 KB
  max_size = 1024 * 1024 # 1 MB
  if request.method == 'POST':
    form = FineTuneForm(request.POST, request.FILES)
    if form.is_valid():
      user_key = form.cleaned_data['user_key']
      # Validate user key
      if not (user_key.startswith("sk-") and 50 < len(user_key) < 60):
        return JsonResponse({"error": "Invalid user key"}, status=400)

      folder_name = random_str()

      files = request.FILES.getlist('file')
      for file in files:
        file_size = file.size
        if file_size < min_size or file_size > max_size:
          return JsonResponse({"error": "Invalid file size"}, status=400)
        if not is_encoding(file, "utf-8"):
          return JsonResponse({"error": "Not correct kind of text file. Please resave as UTF-8"}, status=400)
        if (
          file
          and file.filename.endswith(("txt", "text"))
          and file.mimetype == "text/plain"
        ):
          random_filename = f"{random_str()}.txt"
          default_storage.save(f'finetune/{folder_name}/{random_filename}', file)
        else:
          return JsonResponse({"error": "File is not a text file"}, status=400)
        #threading.Thread(target=train, args=(folder_name, form.cleaned_data['role'], user_key, form.cleaned_data['chunk_type'])).start()
        return JsonResponse({"success": True, "user_folder": folder_name.split("/")[-1]})

  else:
    form = FineTuneForm()

  return render(request, 'finetune.html', {'form': form})

def convert_ebook(request):

  supported_mimetypes = [
  "application/epub+zip", 
  "application/pdf", 
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain"
  ]
  
  if request.method == 'POST':
    form = ConvertEbookForm(request.POST, request.FILES)
    if form.is_valid():
      book_title = form.cleaned_data["book_title"]
      author_name = form.cleaned_data["author_name"]
      uploaded_file = request.FILES.getlist("file")
      folder_name = random_str()

      if uploaded_file:
        if uploaded_file.mimetype not in supported_mimetypes:
          return JsonResponse({"error": "Unsupported file type"}, status=400)
        if uploaded_file.mimetype == "text/plain" and not is_encoding(uploaded_file, "utf-8"):
          return JsonResponse({"error": "Not correct kind of text file. Please resave as UTF-8"}, status=400)
        random_filename = f"{random_str()}.txt"
        file_path = f'convert_file/{folder_name}/{random_filename}'
        default_storage.save(file_path, uploaded_file)

      metadata = {"title": book_title, "author": author_name}
      #output_file = convert_file(file_path, metadata)
      output_file = metadata
      output_filepath = os.path.join(folder_name, output_file)
      response = FileResponse(open(output_filepath, 'rb'), content_type='text/plain')
      response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(output_filepath)
      response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
      response['Pragma'] = 'no-cache'
      response['Expires'] = '0'
        
      return response
  else:
    form = FineTuneForm()

  return render(request, 'convert-ebook.html', {'form': form})

