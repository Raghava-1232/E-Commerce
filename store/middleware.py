import time
from django.db import connection
from django.conf import settings

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        queries = len(connection.queries)
        
        if duration > 1 or queries > 10:  # Log slow requests
            print(f"Slow request: {request.path} took {duration:.2f}s with {queries} queries")
        
        return response 