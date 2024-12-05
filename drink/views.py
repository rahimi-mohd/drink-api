from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .serializers import DrinkSerializer
from .models import Drink


# Create your views here.
@api_view(["GET", "POST"])
def drink_list(request):
    if request.method == "GET":
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        # return JsonResponse({"drink": serializer.data})
        return Response(serializer.data)

    if request.method == "POST":
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def drink_detail(request, pk):
    drink = get_object_or_404(Drink, pk=pk)

    if request.method == "GET":
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    # put is edit, it's work almost the same as POST,
    # but this time editing existed instances
    # instead of adding new instance.
    elif request.method == "PUT":
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    elif request.method == "DELETE":
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
