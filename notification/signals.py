from django.db.models.signals import post_save
from django.dispatch import receiver


from PIL import Image

from post.models import Post
from users.models import User
from comment.models import Comment


from .models import Notification


@receiver(signal=post_save, sender=Post)
def like_notification(sender, instance, created, *args, **kwargs):
    if created:
        return


@receiver(signal=post_save, sender=Comment)
def comment_notification(sender, instance, created, *args, **kwargs):
    """
    {
        id: nkd18d78sd28s78s7d8,
        sender: { name:mahamed, ...},
        recipient: { name:admin, ...},
        action: 'commented on your post'
        hint: 'Who Likes Me',
        hint_img: 'media/files/action-path/image-4.png'

        # content:'Mahamed Toure commented on your post Who Likes Me'
        created_at: 12-07-22
    }


    """
    if created:
        shortcut = Utils()
        notification = Notification()
        notification.action = shortcut.action(instance)
        notification.hint = shortcut.hint(instance)
        notification.hint_img = shortcut.hint_img(instance)
        notification.sender = instance.author
        notification.recipient = shortcut.get_data(instance)["issued_on"].author
        notification.save()


class Utils:
    def action(self, comment):
        data = self.get_data(comment)
        if data["type"] == "parent" and data["issued_on"] == comment.post:
            return "commented on your post"

        if data["type"] == "child":
            return "replies on your comment"
        return ""

    def hint(self, comment):
        if isinstance(self.get_data(comment)["issued_on"], Post):
            if not self.hint_img(comment):
                return self.get_post_field(comment.post)

        if isinstance(self.get_data(comment)["issued_on"], Comment):
            if not self.hint_img(comment):
                return self.get_comment_field(comment)

    def hint_img(self, comment: Comment):
        if isinstance(self.get_data(comment)["issued_on"], Post):
            if not isinstance(self.get_post_field(comment.post), str):
                return self.resize_hint_img(comment.post)

        if isinstance(self.get_data(comment)["issued_on"], Comment):
            if not isinstance(self.get_comment_field(comment), str):
                return self.resize_hint_img(self.get_comment_field(comment))

    def get_data(self, comment: Comment):
        data = {
            "type": "parent",
            "issued_on": None,
        }

        if comment.post:
            data["issued_on"]: Post = comment.post

        if comment.parent:
            data["issued_on"]: Comment = comment
            data["type"]: str = "child"

        return data

    def get_post_field(self, post: Post):
        if post.caption:
            return post.caption[:20]
        elif post.excerpt:
            return post.excerpt[:20]
        elif post.hashtags:
            return post.hashtags[:20]
        elif post.picture:
            return post.picture
        elif post.video:
            return post.video

    def get_comment_field(self, comment: Comment):
        if comment.parent and comment.parent.content:
            return comment.parent.content[:20]
        elif comment.file:
            return comment.file
        elif comment.picture:
            return comment.picture

    def resize_hint_img(self, post: Post):
        if post.video and post.picture:
            return post.video.file.url
        elif post.picture:
            return post.picture.image.url
        else:
            return ""

        path, ext = "", ""
        path_list = post.picture.path.split(".")
        url_path_list = post.picture.path.split(".")

        prefix = "__not___."

        if len(path_list) < 3:
            path = path_list[0]
            ext = path_list[1]

        elif len(path_list) > 2:
            path = path_list[0] + path_list[1]
            ext = path_list[2]

        full_path = path + prefix + ext

        if len(url_path_list) < 3:
            path = url_path_list[0]
            ext = url_path_list[1]

        elif len(url_path_list) > 2:
            path = url_path_list[0] + url_path_list[1]
            ext = url_path_list[2]

        full_url_path = path + prefix + ext

        img = Image.open(post.picture.path).copy()

        thumbnail = (50, 50)
        img.thumbnail(thumbnail)

        img.save(full_path)

        return full_url_path

    # ? Scalable
