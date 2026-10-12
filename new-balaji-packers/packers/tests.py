from django.test import TestCase, Client
from django.urls import reverse
from packers.models import Branch, BookingOrder, CustomerReview


class PackersModelTests(TestCase):
    def setUp(self):
        self.branch_main = Branch.objects.create(
            city='Vuyyuru',
            is_head_office=True,
            badge='Head Office / Main Branch',
            address='Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru',
            phone='9014331173'
        )
        self.branch_vja = Branch.objects.create(
            city='Vijayawada',
            is_head_office=False,
            badge='Branch Office',
            address='Opp. Nagarjuna Hospital, Kanuru, Auto Nagar, Vijayawada',
            phone='9803558899'
        )

    def test_branch_str_and_properties(self):
        self.assertIn("Head Office", str(self.branch_main))
        self.assertTrue(self.branch_main.is_head_office)
        self.assertFalse(self.branch_vja.is_head_office)

    def test_booking_order_creation(self):
        order = BookingOrder.objects.create(
            name="Mr. Suresh Rao",
            phone="9014331173",
            pickup_city="Vuyyuru",
            drop_city="Vijayawada",
            selected_items="2 BHK House items",
            custom_items="1 Double door fridge, 2 ACs",
            estimated_price=6500.00
        )
        self.assertEqual(order.status, 'PENDING')
        self.assertIn("Mr. Suresh Rao", str(order))

    def test_customer_review_creation(self):
        review = CustomerReview.objects.create(
            reviewer_name="Anita K.",
            city="Machilipatnam",
            rating=5,
            review_text="Excellent shifting experience with New Balaji!"
        )
        self.assertTrue(review.is_approved)
        self.assertIn("5★", str(review))


class PackersViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.branch = Branch.objects.create(
            city='Vuyyuru',
            is_head_office=True,
            badge='Head Office / Main Branch',
            address='Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru',
            phone='9014331173'
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Balaji Packers and Movers')
        self.assertContains(response, 'Vuyyuru')
        self.assertContains(response, 'Price Calculator')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mr. Kumar')
        self.assertContains(response, 'Thotlavallaru Road')

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '9014331173')
        self.assertContains(response, 'Vijayawada')
        self.assertContains(response, 'Machilipatnam')

    def test_quote_get_view(self):
        response = self.client.get(reverse('quote'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Shifting Order Request')

    def test_quote_post_valid_form(self):
        post_data = {
            'name': 'Gopal Sharma',
            'phone': '9803558899',
            'email': 'gopal@example.com',
            'pickup_city': 'Vuyyuru',
            'drop_city': 'Vijayawada',
            'items_checkbox': ['1 BHK House items', 'Car Transport'],
            'custom_items': '1 Royal Enfield Bike, 1 TV 55-inch',
            'estimated_price': '6200.00',
            'notes': 'Please arrange morning 8 AM loading.'
        }
        response = self.client.post(reverse('quote'), post_data)
        self.assertRedirects(response, reverse('thanks'))
        
        # Verify saved in database
        order = BookingOrder.objects.filter(phone='9803558899').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.name, 'Gopal Sharma')
        self.assertIn('Royal Enfield', order.custom_items)

    def test_quote_post_invalid_phone(self):
        post_data = {
            'name': 'Invalid User',
            'phone': '123',  # too short
            'pickup_city': 'Vuyyuru',
            'drop_city': 'Vijayawada',
        }
        response = self.client.post(reverse('quote'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(BookingOrder.objects.filter(name='Invalid User').exists())

    def test_submit_review_view(self):
        post_data = {
            'reviewer_name': 'K. Mohan',
            'city': 'Vuyyuru',
            'rating': 5,
            'review_text': 'Superb shifting work by Mr. Kumar and crew.'
        }
        response = self.client.post(reverse('submit_review'), post_data)
        self.assertEqual(response.status_code, 302)
        review = CustomerReview.objects.filter(reviewer_name='K. Mohan').first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
