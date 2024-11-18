from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD
class ButtonUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
=======
class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
>>>>>>> 198f3908512779f0f3c28f02e201c9642d9a8ce5
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
<<<<<<< HEAD
        return f"{self.user.username if self.user else 'Guest'} - {self.message} at {self.timestamp}"
=======
        return f"{self.user.username if self.user else 'Guest'} - {self.message} - {self.timestamp}"
>>>>>>> 198f3908512779f0f3c28f02e201c9642d9a8ce5
