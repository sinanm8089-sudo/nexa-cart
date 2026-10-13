"""
Seed Realistic Customer Reviews for NexaCart products.
Includes realistic price sentiment, build quality feedback, and value perceptions.
"""
import os
import sys
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps'))
django.setup()

from products.models import Product
from accounts.models import User
from reviews.models import Review

# Review pools tailored by price perception & categories
REVIEW_TEMPLATES = [
    # Positive / Great Value
    {
        "rating": 5,
        "title": "Unbeatable value for the price!",
        "comment": "Honestly surprised by the quality at this price point. It performs just as well as alternatives costing 25% more. Battery life and build exceeded my expectations."
    },
    {
        "rating": 5,
        "title": "Worth every single rupee",
        "comment": "Premium materials, buttery smooth performance, and zero heating issues. Worth every penny, would gladly buy again!"
    },
    {
        "rating": 4,
        "title": "Solid daily driver, very fair pricing",
        "comment": "Good bang for the buck. The display is vibrant and specs are top notch. Minor gripe is slightly slow charging, but given the competitive price, can't complain."
    },
    {
        "rating": 4,
        "title": "Great features for the cost",
        "comment": "Very satisfied with this purchase. Comparable products from major brands are ₹10,000 more expensive for similar specs. Well engineered."
    },
    # Mixed / Price Sensitive
    {
        "rating": 3,
        "title": "Good performance, but slightly overpriced",
        "comment": "Performance is acceptable, but at this retail price, they should have included faster charging and a premium case. Would recommend waiting for a ₹3,000 - ₹5,000 price drop or sale."
    },
    {
        "rating": 3,
        "title": "Decent, but competition offers better specs for less",
        "comment": "It works fine for everyday tasks, but rival models offer double the storage and better warranty at roughly the same price. Price feels 10-15% too high right now."
    },
    {
        "rating": 2,
        "title": "Overpriced for what you actually get",
        "comment": "Feels cheap in the hand despite the hefty price tag. Customer support was slow and the features feel half-baked. If the price was ₹5,000 lower it might make sense, but at the current cost it is disappointing."
    },
    {
        "rating": 5,
        "title": "Absolute powerhouse for work and creative tasks",
        "comment": "The speed and screen color accuracy are astounding. If you are a professional, the premium cost is completely justified by how much time it saves."
    },
    {
        "rating": 4,
        "title": "Exceptional ergonomics, reasonably priced",
        "comment": "Lightweight, stylish, and comfortable. Price is reasonable compared to competitors in the market."
    },
    {
        "rating": 1,
        "title": "Too expensive for subpar durability",
        "comment": "Stopped working properly after just 3 weeks of normal use. Way too expensive for this level of quality control. Would not recommend at this price."
    }
]

def seed_reviews():
    users = list(User.objects.filter(role=User.Role.CUSTOMER))
    if not users:
        print("No customer users found. Please run seed_data.py first.")
        return

    products = list(Product.objects.all())
    print(f"Seeding reviews across {len(products)} products with {len(users)} users...")

    created_count = 0
    for product in products:
        # Choose 3 to 6 random users to review each product
        num_reviews = min(random.randint(3, 6), len(users))
        selected_users = random.sample(users, k=num_reviews)

        for user in selected_users:
            if Review.objects.filter(product=product, user=user).exists():
                continue

            # Pick template
            tpl = random.choice(REVIEW_TEMPLATES)
            Review.objects.create(
                product=product,
                user=user,
                rating=tpl["rating"],
                title=tpl["title"],
                comment=tpl["comment"]
            )
            created_count += 1

    print(f"Successfully created {created_count} reviews!")
    print(f"Total reviews in database: {Review.objects.count()}")

if __name__ == "__main__":
    seed_reviews()
