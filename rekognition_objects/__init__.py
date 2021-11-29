from PIL import Image, ImageDraw
import constant
import io


def show_bounding_boxes(image_bytes, image_name, box_sets, colors):
    """
    Draws bounding boxes on an image and shows it with the default image viewer.

    :param image_name: The image name.
    :param image_bytes: The image to draw, as bytes.
    :param box_sets: A list of lists of bounding boxes to draw on the image.
    :param colors: A list of colors to use to draw the bounding boxes.
    """
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    for boxes, color in zip(box_sets, colors):
        for box in boxes:
            left = image.width * box['Left']
            top = image.height * box['Top']
            right = (image.width * box['Width']) + left
            bottom = (image.height * box['Height']) + top
            draw.rectangle([left, top, right, bottom], outline=color, width=3)
    image.save(f'{constant.final_image_folder}/{image_name}')


def show_polygons(image_bytes, image_name, polygons, color):
    """
    Draws polygons on an image and shows it with the default image viewer.

    :param image_name: The image name.
    :param image_bytes: The image to draw, as bytes.
    :param polygons: The list of polygons to draw on the image.
    :param color: The color to use to draw the polygons.
    """
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    for polygon in polygons:
        draw.polygon([
            (image.width * point['X'], image.height * point['Y']) for point in polygon],
            outline=color)
    image.save(f'{constant.final_image_folder}/{image_name}')

