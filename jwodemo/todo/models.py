from django.db import models

class TodoItem(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )
    is_done = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']  # Ensure default ordering is by 'order'

    def __str__(self):
        return self.name
