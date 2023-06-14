# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ManageClassSerializers
from skymarkApp.models import ManageClass
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(['GET'])
def getDataFromManageClassTable(request):
    get_data = ManageClass.objects.all()
    serilializer = ManageClassSerializers(get_data, many=True)
    return Response(serilializer.data)


@api_view(['POST'])
def postDataToManageClassTable(request):
    serializer = ManageClassSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def getOrPutOrDeleteDataFromManageClassTable(request, id):
    try:
        get_data = get_object_or_404(ManageClass, id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ManageClassSerializers(get_data, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ManageClassSerializers(
            get_data, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        serializer = get_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
