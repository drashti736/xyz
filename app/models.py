from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    CHOICE = (
        ('brand', 'Brand'),
        ('influencer', 'Influencer'),
    )
    
    role = models.CharField(max_length=20, choices=CHOICE)


class InfluencerProfile(models.Model):

    # ================= BASIC INFO =================
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="influencer_profiles/")
    full_name = models.CharField(max_length=150)
    bio = models.TextField()
    niche = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    # ================= SOCIAL MEDIA =================
    instagram_username = models.CharField(max_length=150, blank=True, null=True)
    instagram_followers = models.PositiveIntegerField(default=0)

    youtube_channel_link = models.URLField(blank=True, null=True)
    youtube_subscribers = models.PositiveIntegerField(default=0)

    tiktok_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)

    engagement_rate = models.FloatField(help_text="Enter percentage value", blank=True, null=True)
    average_views = models.PositiveIntegerField(blank=True, null=True)

    # ================= PROFESSIONAL DETAILS =================
    years_of_experience = models.PositiveIntegerField(default=0)
    previous_collaborations = models.TextField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    media_kit = models.FileField(upload_to="media_kits/", blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)

    CONTENT_CHOICES = (
        ('reels', 'Reels'),
        ('shorts', 'Shorts'),
        ('stories', 'Stories'),
        ('posts', 'Posts'),
        ('long_videos', 'Long Videos'),
    )
    content_type = models.CharField(max_length=20, choices=CONTENT_CHOICES, blank=True, null=True)

    # ================= PRICING =================
    price_per_reel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per_post = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per_story = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    package_details = models.TextField(blank=True, null=True)
    negotiable = models.BooleanField(default=True)

    # ================= AUDIENCE INSIGHTS =================
    audience_gender_percentage = models.CharField(max_length=100, blank=True, null=True)
    audience_age_group = models.CharField(max_length=100, blank=True, null=True)
    top_audience_country = models.CharField(max_length=100, blank=True, null=True)
    audience_interests = models.TextField(blank=True, null=True)

    # ================= AVAILABILITY =================
    AVAILABLE_FOR_CHOICES = (
        ('paid_collab', 'Paid Collaborations'),
        ('affiliate', 'Affiliate Marketing'),
        ('reviews', 'Product Reviews'),
        ('events', 'Event Appearances'),
    )
    available_for = models.CharField(max_length=20, choices=AVAILABLE_FOR_CHOICES, blank=True, null=True)

    available_from = models.DateField(blank=True, null=True)
    available_to = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name    


class Brand(models.Model):

    INDUSTRY_CHOICES = [
        ('fashion', 'Fashion'),
        ('tech', 'Tech'),
        ('beauty', 'Beauty'),
        ('food', 'Food'),
        ('fitness', 'Fitness'),
        ('education', 'Education'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    business_email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)

    # About Section
    description = models.TextField()
    target_audience = models.CharField(max_length=255)
    mission = models.TextField(blank=True, null=True)

    year_established = models.PositiveIntegerField(blank=True, null=True)
    company_size = models.CharField(max_length=100, blank=True, null=True)
    usp = models.CharField(max_length=255, blank=True, null=True)

    # Social Media
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name    

class Campaign(models.Model):

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
    ]

    FOLLOWER_RANGE = [
        ('1k-10k', '1K-10K (Nano)'),
        ('10k-50k', '10K-50K (Micro)'),
        ('50k-500k', '50K-500K (Macro)'),
    ]

    COLLAB_TYPE = [
        ('paid', 'Paid Promotion'),
        ('affiliate', 'Affiliate Marketing'),
        ('barter', 'Barter Collaboration'),
        ('giveaway', 'Giveaway Campaign'),
        ('ambassador', 'Brand Ambassador'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="campaigns")

    title = models.CharField(max_length=200)
    description = models.TextField()

    influencer_category = models.CharField(max_length=100)
    preferred_platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    follower_range = models.CharField(max_length=50, choices=FOLLOWER_RANGE)

    budget = models.DecimalField(max_digits=10, decimal_places=2)
    campaign_duration = models.CharField(max_length=100)

    collaboration_type = models.CharField(max_length=50, choices=COLLAB_TYPE)

    deliverables = models.TextField(help_text="Example: 2 reels + 3 stories")
    number_of_posts = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Application(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    influencer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    message = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    pay_status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.influencer.username} - {self.campaign.title}"
    


class CollaborationRequest(models.Model):
    brand = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_collabs")
    influencer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_collabs")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    message = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject    
    
    
    
class Payment(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.email} - ₹{self.amount} - {self.status}"    