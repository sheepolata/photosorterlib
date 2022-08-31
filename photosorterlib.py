from PIL import Image
from PIL.ExifTags import TAGS


def get_meta_data(image):
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    exif_data = image.getexif()
    for tag_id in exif_data:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exif_data.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag] = data

    return info_dict


def test():
    image_path = "./Photos/IMG_0002.JPG"
    image = Image.open(image_path)

    md = get_meta_data(image)
    print(md)
