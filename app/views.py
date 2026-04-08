from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Campaign, InfluencerProfile, Brand, Application, CollaborationRequest, Contact, Payment
from .forms import InfluencerProfileForm, BrandForm, CampaignForm
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import stripe
from django.db.models import Exists, OuterRef
# Create your views here.

User = get_user_model()


def home(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = authenticate(username=username, password=password)
        if user is not None:    
            if user.role != role:
                return render(request, 'login.html',{'error_msg' : "Please Select Currect Role"} )
            auth_login(request, user)
            return  redirect('home')
        else:
            return render(request, 'login.html', {'error_msg' : "Username and Password is not valid"})
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error_msg': "Username already exists"
            })
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        return redirect('login')    
    return render(request, 'signup.html')

@login_required
def marketplace(request):
    allinfluencer = InfluencerProfile.objects.all()

   
    return render(
        request,
        'marketplace.html',
        {'allinfluencer': allinfluencer}
    )


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def apply_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    # You can add application logic here later
    return render(request, 'apply_campaign.html', {'campaign': campaign})


@login_required
def contact(request):

    if request.method == "POST":

        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save in database
        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )

        # Send Email
        send_mail(
            subject,
            f"""
New Contact Message

Name: {first_name} {last_name}
Email: {email}

Message:
Thank For Connecting with us
            """,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        return redirect('contact')

    return render(request, 'contact.html')

@login_required
def brand(request):
    return render(request, 'brand.html')

@login_required
def influencer(request):
    
    return render(request, 'influencer.html')

@login_required
def influencer_dashboard(request):
    profile = InfluencerProfile.objects.filter(user=request.user).first()

    # All campaigns
    campaigns = Campaign.objects.all()

    # Applications by this influencer
    applications = Application.objects.filter(
        influencer=request.user
    ).select_related('campaign')

    # Get applied campaign IDs
    applied_campaign_ids = applications.values_list('campaign_id', flat=True)

    # Only campaigns not applied yet
    available_campaigns = campaigns.exclude(id__in=applied_campaign_ids)
    received_requests = CollaborationRequest.objects.filter(
        influencer=request.user,
    )
    return render(request, 'influencerdashboard.html', {
        'profile': profile,
        'available_campaigns': available_campaigns,
        'applications': applications,
        "requests": received_requests
    })



@login_required
def edit_profile(request):
    profile = InfluencerProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = InfluencerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            influencer = form.save(commit=False)
            influencer.user = request.user
            influencer.save()
            return redirect('influencer_dashboard')
    else:
        form = InfluencerProfileForm(instance=profile)

    return render(request, 'edit_influencer_profile.html', {'form': form})

@login_required
def influencer_profile(request, pk):
    profile = InfluencerProfile.objects.get(id=pk)
    
    return render(request, 'influencer_profile.html', {'profile': profile})

@login_required
def influencer_campaigns(request):
    campaigns = Campaign.objects.all()
    return render(request, 'influencer_campaigns.html', {
        'campaigns': campaigns
    })


#-----------------  Brand Start ------------------ #

@login_required
def brand_profile(request):
    brand = Brand.objects.filter(user=request.user).first()
    return render(request, 'brandprofile.html', {'brand': brand})


@login_required
def brand_dashboard(request):

    brand = Brand.objects.filter(user=request.user).first()

    payments = Payment.objects.filter(brand=brand)

    applications = Application.objects.filter(
        campaign__brand=brand
    ).annotate(
        is_paid=Exists(
            Payment.objects.filter(application=OuterRef('pk'))
        )
    ).select_related('campaign', 'influencer').order_by('-applied_at')

    inf_requests = CollaborationRequest.objects.filter(brand=request.user)

    return render(request, 'branddashboard.html', {
        'brand': brand,
        'applications': applications,
        'inf_requests': inf_requests,
    })

@login_required
def edit_brand_profile(request):
    brand = Brand.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand_obj = form.save(commit=False)

            # If brand does not exist yet
            if brand is None:
                brand_obj.user = request.user

            brand_obj.save()
            return redirect('brand_dashboard')
    else:
        form = BrandForm(instance=brand)

    return render(request, 'edit_brand_profile.html', {'form': form})

@login_required
def all_brands(request):
    brands = Brand.objects.all()
    return render(request, 'all_brands.html', {'brands': brands})

def view_brand(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    return render(request, 'brandprofile.html', {'brand': brand})



@login_required
def approve_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    # Security check: only campaign owner can approve
    if application.campaign.brand.user == request.user:
        application.status = 'approved'
        application.save()

    return redirect('brand_dashboard')


@login_required
def reject_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    # Security check
    if application.campaign.brand.user == request.user:
        application.status = 'rejected'
        application.save()

    return redirect('brand_dashboard')


#---------------- Campaign Start ----------------#


@login_required
def create_campaign(request):
    
    brand = Brand.objects.filter(user=request.user).first()
    if not brand:
        return redirect('edit_brand_profile')
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.brand = brand
            campaign.save()
            return redirect('brand_dashboard')
    else:
        form = CampaignForm()

    return render(request, 'create_campaign.html', {'form': form})


@login_required
def brand_campaigns(request):
    brand = Brand.objects.filter(user=request.user).first()
    campaigns = Campaign.objects.filter(brand=brand)
    return render(request, 'my_campaigns.html', {'campaigns': campaigns})


@login_required
def all_campaigns(request):
    campaigns = Campaign.objects.select_related('brand').all().order_by('-created_at')
    return render(request, 'all_campaigns.html', {'campaigns': campaigns})


@login_required
def apply_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Prevent duplicate application
    existing = Application.objects.filter(
        campaign=campaign,
        influencer=request.user
    ).first()

    if not existing:
        Application.objects.create(
            campaign=campaign,
            influencer=request.user
        )

    return redirect('influencer_dashboard')


@login_required
def send_collab_request(request, influencer_id):
    influencer_user = get_object_or_404(User, id=influencer_id) 
    brand = Brand.objects.filter(user=request.user).first()
    if not brand:
        return redirect('edit_brand_profile')
    # Get only campaigns created by this brand
    brand_campaigns = Campaign.objects.filter(brand=brand)
    if request.method == "POST":
        campaign_id = request.POST.get("campaign")
        message = request.POST.get("message")

        campaign = Campaign.objects.get(id=campaign_id)

        # Security Check
        if campaign.brand != brand:
            return HttpResponse("Not allowed")

        CollaborationRequest.objects.create(
            brand=request.user,
            influencer=influencer_user,
            campaign=campaign,
            message=message
        )

        return redirect("brand_dashboard")

    context = {
        "influencer": influencer,
        "campaigns": brand_campaigns
    }
    return render(request, "send_collab.html", context)



@login_required
def approve_collab(request, request_id):
    collab_request = get_object_or_404(CollaborationRequest, id=request_id)

    # Make sure only the correct influencer approves
    if collab_request.influencer != request.user:
        return HttpResponse("Not allowed")

    collab_request.status = "approved"
    collab_request.save()

    return redirect("influencer_dashboard")



stripe.api_key = settings.STRIPE_SECRET_KEY



@login_required
def create_checkout_session(request, app_id):
    # Ensure amount is an integer
    app = get_object_or_404(Application, id=app_id)
    
        
    amount = int(app.campaign.budget)
    
    if settings.APP_BASE_URL:
        base_url = settings.APP_BASE_URL
    else:
        base_url = request.build_absolute_uri('/').rstrip('/')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Donation Payment',
                },
                'unit_amount': amount * 100,  # INR in paise
            },
            'quantity': 1,
        }],
        metadata={
            'brand_id': app.campaign.brand.id,
            'influencer_id': app.influencer.id,
            'campaign_id': app.campaign.id,
            'application_id': app.id,
            'amount': app.campaign.budget
        },
        mode='payment',
        success_url=f"{base_url}{reverse('success')}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}{reverse('cancel')}",
    )
    return redirect(session.url, code=303)



@login_required
def success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return HttpResponse("Session ID missing", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        # You can get email & amount from the session object
        customer_email = session.customer_details.email
        amount_paid = session.amount_total / 100  # convert paise to INR

        brand_id = session.metadata.get('brand_id')
        influencer_id = session.metadata.get('influencer_id')
        application_id = session.metadata.get('application_id')
        amount = session.metadata.get('amount')

        # Fetch actual objects
        brand = Brand.objects.get(id=brand_id)
        application = get_object_or_404(Application,  id=application_id)
        influencer = InfluencerProfile.objects.filter(user=application.influencer).first()
        
        if not influencer:
            return HttpResponse("Influencer profile not found")
        
        # Save payment info to DB
        payment = Payment.objects.create(
            brand=brand,
            influencer=influencer,
            application=application,
            amount=amount,
            stripe_session_id=session.id,
            status=session.payment_status
        )
        
        return render(request, 'success.html', {
           
            'amount': amount,
            'payment_id': payment.id,
        })

    except Exception as e:
        return HttpResponse(f"Failed to retrieve session: {str(e)}", status=500)



@login_required
def cancel(request):
    return render(request, 'cancel.html')

