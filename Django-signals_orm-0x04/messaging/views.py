from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
@login_required
def delete_user(request):
    if request.method == 'DELETE':
        user = request.user
        username = user.username
        user.delete()
        return JsonResponse({'message': f'User {username} and related data deleted successfully.'})
    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)
