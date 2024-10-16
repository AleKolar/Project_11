from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Coords, Level, Images, PerevalAdded
from .serializers import UserSerializer, CoordsSerializer, LevelSerializer, ImagesSerializer, PerevalAddedSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class PerevalAddedViewSet(viewsets.ModelViewSet):
    serializer_class = PerevalAddedSerializer
    queryset = PerevalAdded.objects.all()

    def get_serializer_context(self):
        context = super(PerevalAddedViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context


    def retrieve(self, request, pk=None):
        if pk:
            try:
                pereval = PerevalAdded.objects.get(pk=pk)
                serializer = PerevalAddedSerializer(pereval, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PerevalAdded.DoesNotExist:
                return Response({"message": "PerevalAdded not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, partial=False):
        pereval = PerevalAdded.objects.get(pk=pk)
        serializer = PerevalAddedSerializer(pereval, data=request.data, partial=partial,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def submitDataByEmail(self, request, email=None):
        if email:
            perevaladded_items = PerevalAdded.objects.filter(user__email=email)
            serializer = PerevalAddedSerializer(perevaladded_items, many=True, context=self.get_serializer_context())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Введите email пользователя в URL"}, status=status.HTTP_400_BAD_REQUEST)