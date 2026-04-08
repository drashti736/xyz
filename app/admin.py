from django.contrib import admin
from .models import  InfluencerProfile, Campaign, Brand
# Register your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(InfluencerProfile)

admin.site.register(Brand)
admin.site.register(Campaign)

admin.site.register(User)


