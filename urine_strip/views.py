from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UrineStripImage
from .utils import identify_colors
from django.shortcuts import render
from django.http import JsonResponse

@api_view(['GET'])
def index(request):
    return render(request, 'urine_strip/index.html')

@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        colors = identify_colors(image)

        # Save the image and its colors to the database
        urine_strip_image = UrineStripImage(image=image, colors=colors)
        urine_strip_image.save()

        return JsonResponse({'colors': colors}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
