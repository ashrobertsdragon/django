import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError, transaction

from binders.utils import random_str

class UserTable(AbstractUser):
  join_date = models.DateTimeField(auto_now_add=True)
  birthdate = models.DateField(null=True, blank=True)
  name = models.CharField(max_length=50)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  user_folder = models.CharField(max_length=7, unique=True)
  credits = models.IntegerField(default=0)

  def generate_unique_folder(self):
    self.user_folder=random_str()
  def save(self, *args, **kwargs):
    while True:
      if not self.user_folder:  # Generate only if not already set
        self.user_folder = random_str()
      try: # attempt to save random strin as user_folder and regenerate if already used
        with transaction.atomic():
          super().save(*args, **kwargs)
          break
      except IntegrityError:
        continue

class BindersTable(models.Model):
  user = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='submissions')
  author_name = models.CharField(max_length=30)
  book_title = models.CharField(max_length=50)
  binder_type = "LoreBinder" # eventually more than one type of binder

  def __str__(self):
    return f"{self.book_title} by {self.author_name}"
