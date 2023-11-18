from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .models import *
from .filters import EventFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authentication import TokenAuthentication

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)
    
    
class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)
    
class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        event = self.get_object()
        user = self.request.user

        if event in user.saved_events.all():
            return Response({'status': 'Event already added to favorites.'}, status=status.HTTP_400_BAD_REQUEST)

        user.saved_events.add(event)

        return Response({'status': 'Event added to favorites successfully'})

class EventSearchView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    permission_classes = (permissions.AllowAny,)

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def save_event(request, event_id):
#     user = request.user
#     try:
#         event = Event.objects.get(pk=event_id)
#     except Event.DoesNotExist:
#         return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

#     if Event.objects.filter(pk=event_id, users_who_saved=user).exists():
#         return Response({'detail': 'Event already saved.'}, status=status.HTTP_400_BAD_REQUEST)

#     event.users_who_saved.add(user)

#     serializer = EventSerializer(event)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def save_event(request, event_id):
    user = request.user

    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if Event.objects.filter(pk=event_id, users_who_saved=user).exists():
            return Response({'detail': 'Event already saved.'}, status=status.HTTP_400_BAD_REQUEST)

        event.users_who_saved.add(user)

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        if not Event.objects.filter(pk=event_id, users_who_saved=user).exists():
            return Response({'detail': 'Event not found in saved events.'}, status=status.HTTP_404_NOT_FOUND)

        event.users_who_saved.remove(user)
        return Response({'detail': 'Event removed from saved events successfully.'}, status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_events(request):
    user = request.user
    saved_events = user.saved_events.all()
    serializer = EventSerializer(saved_events, many=True)
    return Response(serializer.data)