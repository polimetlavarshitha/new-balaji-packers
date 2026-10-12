import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from packers.models import Branch, CustomerReview

User = get_user_model()


class Command(BaseCommand):
    help = "Pre-populates initial Branch records, initial customer reviews, and creates superuser."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Setting up New Balaji Packers and Movers data..."))

        # 1. Pre-populate Branches
        branches_data = [
            {
                'city': 'Vuyyuru',
                'is_head_office': True,
                'badge': 'Head Office / Main Branch',
                'address': 'Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru',
                'phone': '9014331173',
                'order': 1,
            },
            {
                'city': 'Vijayawada',
                'is_head_office': False,
                'badge': 'Branch Office',
                'address': 'Opp. Nagarjuna Hospital, Kanuru, Auto Nagar, Vijayawada',
                'phone': '9803558899',
                'order': 2,
            },
            {
                'city': 'Machilipatnam',
                'is_head_office': False,
                'badge': 'Branch Office',
                'address': 'Housing Board Colony, Bypass Road, Machilipatnam',
                'phone': '8099333910',
                'order': 3,
            },
        ]

        for b_data in branches_data:
            branch, created = Branch.objects.update_or_create(
                city=b_data['city'],
                defaults=b_data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} branch: {branch.city} (Head Office: {branch.is_head_office})"))

        # 2. Pre-populate Initial Customer Reviews
        reviews_data = [
            {
                'reviewer_name': 'Ramesh V.',
                'city': 'Vijayawada',
                'rating': 5,
                'review_text': "Shifted our 2 BHK house from Vuyyuru Main Branch to Vijayawada seamlessly. Mr. Kumar's team handled all electronics and furniture with great care!",
                'is_approved': True,
            },
            {
                'reviewer_name': 'Priya M.',
                'city': 'Machilipatnam',
                'rating': 5,
                'review_text': "Very safe packing with bubble wrap and secure transportation for our office equipment in Machilipatnam. Highly recommended!",
                'is_approved': True,
            },
            {
                'reviewer_name': 'K. Srinivas',
                'city': 'Vuyyuru',
                'rating': 5,
                'review_text': "Called Mr. Kumar at 9014331173 and received an immediate quote. Timely loading, reliable crew, and official bank approval bill provided promptly.",
                'is_approved': True,
            },
            {
                'reviewer_name': 'Venkat Rao',
                'city': 'Hyderabad -> Vijayawada',
                'rating': 5,
                'review_text': "Car transportation and household goods shifted safely with zero scratches. The price calculator estimate matched our final quote perfectly!",
                'is_approved': True,
            },
        ]

        for r_data in reviews_data:
            CustomerReview.objects.get_or_create(
                reviewer_name=r_data['reviewer_name'],
                defaults=r_data
            )
        self.stdout.write(self.style.SUCCESS("Customer reviews pre-populated."))

        # 3. Create Superuser if needed
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@balajipackers.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully (default password: {password})."))
        else:
            self.stdout.write(self.style.NOTICE(f"Superuser '{username}' already exists."))

        self.stdout.write(self.style.SUCCESS("All initial data setup complete!"))
