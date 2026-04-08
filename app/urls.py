from . import views

from django.urls import path

urlpatterns =[
    path('', views.home , name='home'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact ,name='contact'),
    path('influencer/' ,views.influencer,name='influencer'),
    path('login/' ,views.login,name='login'),
    path('signup/' ,views.signup,name='signup'),
    path('logout/' ,views.logout,name='logout'),
    path('influencer-dashboard/', views.influencer_dashboard, name='influencer_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('influencerprofile/<int:pk>/' ,views.influencer_profile,name='influencerprofile'),
    path('profile/', views.brand_profile, name='brand_profile'),
    path('brand-dashboard/', views.brand_dashboard, name='brand_dashboard'),
    path('brand-dashboard/edit/', views.edit_brand_profile, name='edit_brand_profile'),
    path('dashboard/campaign/create/', views.create_campaign, name='create_campaign'),
    path('dashboard/campaigns/', views.brand_campaigns, name='brand_campaigns'),
    path('campaigns/', views.all_campaigns, name='all_campaigns'),
    path('brands/', views.all_brands, name='allbrand'),
    path('view-brand/<int:pk>', views.view_brand, name='view_brand'),
    path('apply/<int:campaign_id>/', views.apply_campaign, name='apply_campaign'),
    path('application/<int:app_id>/approve/', views.approve_application, name='approve_application'),
    path('application/<int:app_id>/reject/', views.reject_application, name='reject_application'),
    path('collab/send/<int:influencer_id>/', views.send_collab_request, name="send_collab"),
    path("collab/approve/<int:request_id>/", views.approve_collab, name="approve_collab"),
    path('stripe/create-checkout-session/<int:app_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
]