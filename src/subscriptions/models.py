from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from helpers.billing import create_product, create_price


User = settings.AUTH_USER_MODEL  # "auth.USER"
SUBSCRIPTION_PERMISSIONS = [
            ("advanced", "Advanced Perm"),  # subscriptions.advanced
            ("pro", "Pro Perm"),            # subscriptions.pro
            ("basic", "Basic Perm"),        # subscriptions.basic    
            ("basic_ai", "Basic AI Perm"),  # subscriptions.basic_ai
        ]

class Subscriptions(models.Model):
    '''
    Subscription Plan = Stripe Product
    '''
    name = models.CharField(max_length=120)
    subtitle = models.TextField(blank=True, default="")
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission,
    limit_choices_to = {
        "content_type__app_label": "subscriptions",
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS]
    }
    )
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    order = models.IntegerField(default=-1, help_text='Order on Django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured on Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(
        help_text="Features for pricing, seperated by new line",
        blank=True, null=True,
    )

    class Meta:
        ordering = ['order', 'featured', '-updated']
        permissions = SUBSCRIPTION_PERMISSIONS

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_response = create_product(
                                    name=self.name, 
                                    metadata={
                                        "subscription_plan_id": self.id
                                    }, 
                                    raw=False
                                )
            self.stripe_id = stripe_response

        super().save(*args, **kwargs)

    def get_features_as_list(self):
        if not self.features:
            return []
        return [ x.strip() for x in self.features.split("\n")]

class SubscriptionPrice(models.Model):
    INTERVAL = (
        ("day", "Dayly"),
        ("week", "Weekly"),
        ("month", "Monthly"),
        ("year", "Yearly"),
    )
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    interval = models.CharField(max_length=120, default=INTERVAL[2][0], choices=INTERVAL)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text='Order on Django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured on Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subscription__order', 'order', 'featured', '-updated']

    @property
    def get_checkout_url(self):
        return reverse("sub-price-checkout", kwargs={"price_id": self.id})
    
    @property
    def display_features_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()
    
    @property
    def display_sub_name(self):
        if not self.subscription:
            return "Plan"
        return self.subscription.name
    
    @property
    def display_subtitle(self):
        if self.subscription is None:
            return ""
   
        return self.subscription.subtitle
    
    @property
    def stripe_currency(self):
        return "usd"
    
    @property
    def stripe_price(self):
        """
        remove decimal places
        """
        return int(self.price * 100)
    
    @property
    def stripe_interval(self):
        return self.interval
        
    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        if self.stripe_id is None and self.product_stripe_id is not None:
            stripe_response = create_price(
                                currency=self.stripe_currency,
                                unit_amount=self.stripe_price,
                                interval=self.stripe_interval,
                                product=self.product_stripe_id,
                                metadata={
                                        "subscription_plan_price_id": self.id
                                },
                                raw=False
                            )
            self.stripe_id = stripe_response

        super().save(*args, **kwargs)

        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval,
            ).exclude(id=self.id)
            qs.update(featured=False)


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *arg, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups = subscription_obj.groups.all()
    permissions = subscription_obj.permissions.all()

    user.groups.set(groups)
    user.user_permissions.set(permissions)

post_save.connect(user_sub_post_save, sender=UserSubscription)