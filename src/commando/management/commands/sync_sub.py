from django.core.management.base import BaseCommand
from subscriptions.models import Subscriptions


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Subscriptions.objects.filter(is_active=True)

        for obj in qs:
            sub_perms = obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(sub_perms)
