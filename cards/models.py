from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

    
class BusinessProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_cards')
    unique_name = models.SlugField(unique=True)
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    google_review_link = models.URLField(blank=True, null=True)
    google_place_id = models.CharField(max_length=250, blank=True, null=True)
    google_map = models.URLField(blank=True, null=True)

    
    def __str__(self):
        return self.business_name
    
    # @property
    # def google_review_link(self):
    #     if self.google_place_id:
    #         return f"https://search.google.com/local/writereview?placeid={self.google_place_id}"
    #     return None

class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField(upload_to='social_icons/', blank=True, null=True)

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform} - {self.profile.business_name}"


class Service(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    # Optional: image upload
    image = models.ImageField(upload_to='service/', blank=True, null=True)

    # Optional: use an icon name (e.g., "fa-solid fa-user")
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome or similar icon class")

    description = models.TextField()

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.profile.business_name}"


class PhoneNumber(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number


class BusinessProfileSEO(models.Model):
    profile = models.OneToOneField('BusinessProfile', on_delete=models.CASCADE, related_name='seo')

    # Basic SEO
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords")

    # Open Graph (OG) for social sharing
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='seo/og_images/', blank=True, null=True)

    # Twitter Card
    twitter_title = models.CharField(max_length=255, blank=True)
    twitter_description = models.TextField(blank=True)
    twitter_image = models.ImageField(upload_to='seo/twitter_images/', blank=True, null=True)

    # Canonical URL
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"SEO for {self.profile.business_name}"
    

class TrackingConfig(models.Model):
    profile = models.OneToOneField('BusinessProfile', on_delete=models.CASCADE, related_name='tracking')

    google_analytics_id = models.CharField(max_length=50, blank=True, help_text="e.g. UA-XXXXX-Y or G-XXXXXXX")
    facebook_pixel_id = models.CharField(max_length=50, blank=True, help_text="e.g. 123456789012345")
    google_tag_manager_id = models.CharField(max_length=50, blank=True, help_text="e.g. GTM-XXXXXX")

    def __str__(self):
        return f"Tracking for {self.profile.business_name}"


class ThemeTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    preview_image = models.ImageField(upload_to='theme_templates/', blank=True, null=True)

    def __str__(self):
        return self.name

class ThemeSetting(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='theme_setting')
    theme_template = models.OneToOneField(ThemeTemplate, on_delete=models.CASCADE, related_name='template', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#000000')  # hex color
    secondary_color = models.CharField(max_length=7, default='#ffffff')
    third_color = models.CharField(max_length=7, default='#ffffff')
    font_color = models.CharField(max_length=7, default='#ffffff')
    font_family = models.CharField(max_length=100, default='Arial')


    def __str__(self):
        return f"Theme Settings for {self.profile.business_name}"


class ProfileSettings(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='profile_setting')
    show_logo = models.BooleanField(default=True)
    show_social_links = models.BooleanField(default=True)
    show_contact_info = models.BooleanField(default=True)
    show_services = models.BooleanField(default=True)
    show_gallery = models.BooleanField(default=True)
    show_map = models.BooleanField(default=True)

    def __str__(self):
        return f"Theme Settings for {self.profile.business_name}"