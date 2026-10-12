from django import forms
import re
from .models import BookingOrder, CustomerReview

CITY_CHOICES = [
    ('Vuyyuru', 'Vuyyuru (Head Office)'),
    ('Vijayawada', 'Vijayawada (Branch)'),
    ('Machilipatnam', 'Machilipatnam (Branch)'),
    ('Guntur', 'Guntur'),
    ('Hyderabad', 'Hyderabad'),
    ('Rajahmundry', 'Rajahmundry'),
    ('Visakhapatnam', 'Visakhapatnam'),
    ('Other Location', 'Other Location (Pan India)'),
]

STANDARD_ITEMS = [
    ('1 BHK House items', '1 BHK House Items'),
    ('2 BHK House items', '2 BHK House Items'),
    ('3+ BHK House items', '3+ BHK House Items'),
    ('Office Goods', 'Office Furniture & Computers'),
    ('Car Transport', 'Car / Vehicle Transport'),
    ('Single Heavy Items', 'Single Heavy Appliances (Fridge / Washing Machine / Sofa)'),
]


class BookingOrderForm(forms.ModelForm):
    """
    ModelForm for customer booking order requests.
    Supports standard item checkboxes and manual custom items input with CSRF protection.
    """
    pickup_city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'id': 'id_pickup_city',
        }),
        label="Pickup City (From)"
    )

    drop_city = forms.ChoiceField(
        choices=CITY_CHOICES,
        initial='Vijayawada',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'id': 'id_drop_city',
        }),
        label="Drop City (To)"
    )

    class Meta:
        model = BookingOrder
        fields = [
            'name',
            'phone',
            'email',
            'pickup_city',
            'drop_city',
            'move_date',
            'selected_items',
            'custom_items',
            'estimated_price',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your full name',
                'required': 'required',
                'id': 'id_name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. 9014331173 or 9803558899',
                'required': 'required',
                'type': 'tel',
                'id': 'id_phone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'optional email address',
                'id': 'id_email',
            }),
            'move_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_move_date',
            }),
            'selected_items': forms.HiddenInput(attrs={
                'id': 'id_selected_items',
            }),
            'custom_items': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., 1 Double Door Fridge, 2 ACs (1.5 ton), 1 Sofa Set (3+1+1), 1 Dining Table, 1 TV 55-inch, 1 Royal Enfield Bike...',
                'id': 'id_custom_items',
            }),
            'estimated_price': forms.HiddenInput(attrs={
                'id': 'id_estimated_price',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any specific floor, lift availability, or special packing requirements...',
                'id': 'id_notes',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10:
            raise forms.ValidationError('Please enter a valid 10-digit phone number so Mr. Kumar can contact you.')
        return phone


class CustomerReviewForm(forms.ModelForm):
    """
    ModelForm for customer reviews with live star rating selector.
    """
    class Meta:
        model = CustomerReview
        fields = ['reviewer_name', 'city', 'rating', 'review_text']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': 'required',
                'id': 'id_reviewer_name',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Vuyyuru or Vijayawada',
                'id': 'id_review_city',
            }),
            'rating': forms.HiddenInput(attrs={
                'id': 'id_rating_input',
                'value': '5',
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience with New Balaji Packers and Movers...',
                'required': 'required',
                'id': 'id_review_text',
            }),
        }
