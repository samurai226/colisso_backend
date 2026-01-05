from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


class HealthCheckView(APIView):
    """
    Health check endpoint to verify the API is running
    """
    permission_classes = []
    
    def get(self, request):
        try:
            # Test database connection
            connection.ensure_connection()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        return Response({
            "status": "ok",
            "message": "Colisso API - Module 1 is running!",
            "database": db_status,
            "module": "CORE",
        }, status=status.HTTP_200_OK)
