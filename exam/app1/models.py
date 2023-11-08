from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name="User's profile",
        editable=True,
        blank=True,
        null=True,
        default=None,
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
        unique=True
    )
    avatar = models.ImageField(verbose_name="Avatar", upload_to="static/images/profile_av", default="/static/images/profile_av/person-circle.svg", blank=True)
    class Meta:
        app_label = 'auth'
        ordering = ("user",)

    def __str__(self):
        return f"profile_{self.user.username}"



@receiver(post_save, sender=User)
def auto_user_model(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)



class Post(models.Model):
    author = models.ForeignKey(verbose_name="Author", to=User, on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name="Title", max_length=200)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(verbose_name="Picture", upload_to="static/images/posts", null=True, default=None)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    date_time = models.DateTimeField(verbose_name="Date", default=now)

    class Meta:
        app_label = "app1"
        ordering = ("-date_time",)
        verbose_name = "Post"

    def __str__(self):
        return f"({self.id})_{self.title}"

class PostComments(models.Model):
    post = models.ForeignKey(verbose_name="Commented post", to=Post, on_delete=models.CASCADE)
    author = models.ForeignKey(verbose_name="Author", to=User, on_delete=models.CASCADE)
    text = models.TextField("Comment", default="", max_length=3500, null=False)
    date_time = models.DateTimeField("Date commented", default=now)

    def __str__(self):
        return f"{self.post}_{self.text[:10]}.."


