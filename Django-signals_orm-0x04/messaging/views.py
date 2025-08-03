from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DeleteUserView(View):
    def delete(self, request):
        user = request.user
        username = user.username
        user.delete()
        return JsonResponse({'message': f'User {username} and related data deleted successfully.'})

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
