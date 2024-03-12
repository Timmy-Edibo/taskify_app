from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


def create_username(request):
    error = ""
    email = request.data.get("email")
    user = CustomUser.objects.filter(email=email).first()

    try:
        last_user_id = CustomUser.objects.last().id + 1
    except ObjectDoesNotExist:
        last_user_id = 1

    if not user:
        username = request.data.get("email").split("@")[0]
        user_name = f"{username}{last_user_id}"
        return user_name, error
    else:
        error = ("Email already exist",)
        return None, error
