from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views import View

from webapp.models import Like


class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content_type = kwargs.get('content_type')
        object_id = kwargs.get('object_id')
        model = ContentType.objects.get(model=content_type).model_class()
        obj = model.objects.get(id=object_id)

        like, created = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            user=request.user
        )

        if created:
            message = 'liked'
        else:
            like.delete()
            message = 'unliked'

        return JsonResponse({
            'likes_count': obj.likes_count(),
            'message': message,
        })