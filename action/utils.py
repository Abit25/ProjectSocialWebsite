import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

def save_action(verb,user,target=None):
    print('Called save_action')
    now=timezone.now()
    print(verb,user,target)

    last_minute=now-datetime.timedelta(seconds=60)

    similar_action = Action.objects.filter(user=user,verb= verb,created__gte=last_minute)
    print('Hey')
    print('Similar Actions are: ')

    if target:

        target_ct=ContentType.objects.get_for_model(target)

        similar_action=similar_action.filter(target_ct=target_ct,target_id=target.id)

    if not similar_action:
        print('No similar_actions')
        Action.objects.create(verb=verb,user=user,target=target)
        print('No similar_actions')

        print('Function executed')
        return True

    return False
