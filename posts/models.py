import os

from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver

from django.urls import reverse

USER_MODEL = get_user_model()


def upload_location(post, filename):
    return f'{post.author_id}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    post_image = models.ImageField(upload_to=upload_location,
                                   null=True, blank=True)

    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='Likes')
    likes = models.ManyToManyField(USER_MODEL, blank=True)

    class Meta:
        ordering = ['-created_timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:details_view", kwargs={"pk": self.pk})


@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file and containing folder from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.post_image:
        if os.path.isfile(instance.post_image.path):
            file_path = instance.post_image.path
            file_dir = os.path.dirname(instance.post_image.path)
            os.remove(file_path)
            if not os.listdir(file_dir):
                os.rmdir(file_dir)


@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    post = Post.objects.get(pk=instance.pk)

    if not post.post_image:
        return False
    else:
        new_file = instance.post_image
        if post.post_image != new_file:
            if os.path.isfile(post.post_image.path):
                os.remove(post.post_image.path)


class Comment(models.Model):
    comment = models.TextField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment if len(self.comment) < 10 else self.comment[:10]


