import mimetypes
from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 10485760  # mega bytes

def validate_file(file):
    mime_type = mimetypes.guess_type(file.name)[0]
    audio_types = ["audio/mpeg", "audio/ogg", "audio/webm" "audio/wav"]
    video_types = ["video/mp4", "video/webm", "video/ogg"]
    image_types = [
        "image/jpeg",
        "image/jpg",
        "image/jpeg",
        "image/gif",
        "image/bmp",
        "image/webp",
    ]
    

    if not file.type in [*mime_type, *audio_types, *video_types, *image_types]:
        msg = 'File type not supported'
        raise ValidationError(msg)