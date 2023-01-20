# Comment
def comment_picture_path(instance, filename):
    return f"comments/imaged/{instance.id}__{filename}"


def comment_file_path(instance, filename):
    return f"comments/files/{instance.id}__{filename}"


# Posts
def post_thumbnail_path(instance, filename):
    return f"posts/{instance.author.username}/id__{instance.caption[:7]}__/thumbn__{filename}"


def post_img_path(instance, filename):
    return f"posts/by_{instance.author.email}/{filename}"


def post_video_path(instance, filename):
    return f"posts/by_{instance.author.email}/{filename}"


# Status
def status_img_path(instance, filename):
    return f"status/{instance.author.email}/img/{filename}"


# Status
def status_video_path(instance, filename):
    return f"status/{instance.author.email}/video/{filename}"


# profile celebrity
def avatar_path(instance, filename):
    return f"profiles/{instance.email}/avater/{filename}"


def cover_img_path(instance, filename):
    return f"profiles/{instance.email}/cover/{filename}"


# Group chat images
def group_chat_img_path(instance, filename):
    return f"groups/{instance.group_set.name}/img/{filename}"


# Group chat video
def group_chat_video_path(instance, filename):
    return f"groups/{instance.group_set.name}/video/{filename}"
