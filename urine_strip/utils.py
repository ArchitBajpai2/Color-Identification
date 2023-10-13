import cv2
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile


def identify_colors(image):
    # Load the image using OpenCV
    if not isinstance(image, InMemoryUploadedFile):
        return {'error': 'Invalid file format'}

    # Read the uploaded file directly from memory
    image_bytes = image.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert the image to the RGB color space (OpenCV loads images in BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Define color regions using color thresholds
    color_regions = {
        'URO': ([170, 100, 100], [230, 170, 170]),
        'BIL': ([160, 90, 60], [220, 180, 160]),
        'KET': ([150, 60, 60], [210, 140, 140]),
        'BLD': ([180, 50, 0], [240, 140, 70]),
        'PRO': ([160, 100, 60], [220, 180, 140]),
        'NIT': ([170, 120, 100], [230, 190, 170]),
        'LEU': ([160, 110, 100], [220, 190, 170]),
        'GLU': ([60, 130, 160], [140, 190, 230]),
        'SG': ([70, 40, 0], [160, 120, 60]),
        'PH': ([100, 60, 0], [230, 170, 120]),
    }

    color_data = {}

    # Iterate through color regions and calculate the average color
    for label, (lower, upper) in color_regions.items():
        mask = cv2.inRange(img_rgb, np.array(lower), np.array(upper))
        masked_image = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)
        
        # Calculate the average color of the masked region
        average_color = np.mean(masked_image, axis=(0, 1), dtype=int)
        color_data[label] = average_color.tolist()

    return color_data

