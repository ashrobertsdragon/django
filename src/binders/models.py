import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError, transaction

from binders.utils import random_str

class UserTable(AbstractUser):
  join_date = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=50, blank=True, null=True)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  user_folder = models.CharField(max_length=7, unique=True, editable=False)
  credits_available = models.IntegerField(default=0)
  credits_used = models.IntegerField(default=0)

  def generate_unique_folder(self):
    while True:
      random_folder = random_str()
      try:
        with transaction.atomic():
          self.user_folder = random_folder
      except IntegrityError:
        continue

  def save(self, *args, **kwargs):
    while True:
      if not self.user_folder:  # Generate only if not already set
        self.user_folder = self.generate_unique_folder()
      super().save(*args, **kwargs)

class BindersTable(models.Model):
  user = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='submissions')
  author_name = models.CharField(max_length=30)
  book_title = models.CharField(max_length=50)
  binder_type = "LoreBinder" # eventually more than one type of binder

  def __str__(self):
    return f"{self.book_title} by {self.author_name}"
