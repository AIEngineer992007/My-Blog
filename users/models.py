import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Kiểm tra an toàn: Có file đính kèm AND file thực sự tồn tại trên ổ đĩa
        if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    new_size = (300, 300)
                    img.thumbnail(new_size)
                    img.save(self.image.path)
            except Exception as e:
                # Bắt ngoại lệ nếu file ảnh bị hỏng hoặc không mở được
                pass