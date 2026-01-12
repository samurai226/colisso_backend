"""
Authentication views
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, UserInfoSerializer


class RegisterView(generics.CreateAPIView):
    """
    Inscription d'un nouvel utilisateur avec rôle CLIENT automatique
    
    POST /api/v1/auth/register/
    {
        "telephone": "+22612345678",
        "nom": "Doe",
        "prenom": "John",
        "email": "john@example.com",
        "password": "motdepasse123",
        "password_confirm": "motdepasse123"
    }
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            # Données utilisateur
            user_data = UserInfoSerializer(user).data
            
            return Response({
                'success': True,
                'message': f'Bienvenue {user.prenom} !',
                'user': user_data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
    Vue de connexion personnalisée
    
    POST /api/v1/auth/login/
    {
        "telephone": "+22612345678",
        "password": "motdepasse123"
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            # Données utilisateur
            user_data = UserInfoSerializer(user).data
            
            return Response({
                'success': True,
                'message': f'Bienvenue {user.prenom} !',
                'user': user_data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """
    Récupérer les infos de l'utilisateur connecté
    
    GET /api/v1/auth/me/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        })