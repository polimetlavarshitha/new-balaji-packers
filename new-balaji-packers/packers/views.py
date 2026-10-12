from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
from .models import Branch, BookingOrder, CustomerReview
from .forms import BookingOrderForm, CustomerReviewForm, STANDARD_ITEMS
from django.shortcuts import render

def home(request):
    return render(request, 'packers/index.html')

def index(request):
    """
    Home page view displaying hero banner, branches, interactive price calculator,
    services, verified reviews, and interactive star rating submission form.
    """
    branches = Branch.objects.all().order_by('order', '-is_head_office')
    reviews = CustomerReview.objects.filter(is_approved=True).order_by('-created_at')[:8]
    review_stats = CustomerReview.objects.filter(is_approved=True).aggregate(
        avg_rating=Avg('rating')
    )
    avg_rating = round(review_stats['avg_rating'] or 4.9, 1)
    review_count = CustomerReview.objects.filter(is_approved=True).count()

    review_form = CustomerReviewForm()

    context = {
        'branches': branches,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'review_form': review_form,
        'standard_items': STANDARD_ITEMS,
    }
    return render(request, 'index.html', context)


def about(request):
    """
    About Us page detailing New Balaji Packers and Movers,
    Proprietor Mr. Kumar, Head Office in Vuyyuru, and branches in Vijayawada & Machilipatnam.
    """
    branches = Branch.objects.all().order_by('order', '-is_head_office')
    return render(request, 'about.html', {'branches': branches})


def contact(request):
    """
    Contact Us page with branch cards, phone numbers, and WhatsApp links.
    """
    branches = Branch.objects.all().order_by('order', '-is_head_office')
    return render(request, 'contact.html', {'branches': branches})


def quote(request):
    """
    Order booking page featuring Django ModelForm with custom item input,
    pre-filled price estimate from the calculator, and CSRF protection.
    """
    if request.method == 'POST':
        form = BookingOrderForm(request.POST)
        # Process custom selected item checkboxes from POST if selected
        selected_items_list = request.POST.getlist('items_checkbox')
        
        if form.is_valid():
            order = form.save(commit=False)
            if selected_items_list:
                order.selected_items = ", ".join(selected_items_list)
            order.save()
            
            # Store in session for confirmation page
            request.session['last_order_id'] = order.id
            request.session['last_customer_name'] = order.name
            
            messages.success(
                request,
                f"Thank you, {order.name}! Your booking request #{order.id} has been received. Mr. Kumar will contact you shortly."
            )
            return redirect('thanks')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        # Pre-fill from GET parameters if coming from interactive price calculator
        initial_data = {}
        if request.GET.get('pickup'):
            initial_data['pickup_city'] = request.GET.get('pickup')
        if request.GET.get('drop'):
            initial_data['drop_city'] = request.GET.get('drop')
        if request.GET.get('estimate'):
            initial_data['estimated_price'] = request.GET.get('estimate')
        if request.GET.get('item'):
            initial_data['selected_items'] = request.GET.get('item')

        form = BookingOrderForm(initial=initial_data)

    branches = Branch.objects.all().order_by('order', '-is_head_office')
    return render(request, 'quote.html', {
        'form': form,
        'standard_items': STANDARD_ITEMS,
        'branches': branches,
    })


def thanks(request):
    """
    Order confirmation view with booking details and prompt contact links.
    """
    order_id = request.session.get('last_order_id')
    customer_name = request.session.get('last_customer_name', 'Valued Customer')
    order = None

    if order_id:
        try:
            order = BookingOrder.objects.get(id=order_id)
        except BookingOrder.DoesNotExist:
            order = None

    return render(request, 'thanks.html', {
        'order': order,
        'customer_name': customer_name,
        'order_id': order_id,
    })


def submit_review(request):
    """
    Handles live customer review submissions with star rating and CSRF protection.
    """
    if request.method == 'POST':
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(
                request,
                f"Thank you, {review.reviewer_name}! Your {review.rating}-star review has been published."
            )
        else:
            messages.error(request, "Unable to submit review. Please ensure your name and review message are filled.")
    return redirect('/#reviews')
