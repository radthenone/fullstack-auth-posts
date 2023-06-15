from datetime import datetime


def avatar_upload_path(instance):
    now = datetime.now()
    path = f'avatars/{now.strftime("%Y/%m/%d")}/{instance.user.email}/'
    return path
