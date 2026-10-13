"""
Synthetic Data Generator for NexaCart
Generates products, users, and simulated interaction traffic
so the recommendation engine can be demonstrated and evaluated.
"""
import os
import sys
import django
import random
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps'))
django.setup()

from django.utils.text import slugify
from accounts.models import User
from products.models import Category, Product, ProductTag
from recommendations.models import Interaction
from orders.models import Order, OrderItem

# ── Categories ──────────────────────────────────────────────────
CATEGORIES = {
    "Electronics": ["Laptops", "Smartphones", "Tablets", "Headphones", "Cameras"],
    "Fashion": ["Men's Clothing", "Women's Clothing", "Shoes", "Accessories"],
    "Beauty & Personal Care": ["Makeup", "Skincare", "Fragrances"],
    "Home & Kitchen": ["Furniture", "Cookware", "Decor", "Appliances"],
    "Books": ["Fiction", "Non-Fiction", "Academic", "Comics"],
    "Sports": ["Fitness", "Outdoor", "Team Sports", "Yoga"],
}

# ── Tags ────────────────────────────────────────────────────────
TAGS = [
    "budget", "premium", "bestseller", "new-arrival", "eco-friendly",
    "gaming", "coding", "travel", "office", "student",
    "lightweight", "waterproof", "wireless", "organic", "handmade",
]

# ── Product templates per subcategory ───────────────────────────
PRODUCTS = {
    "Laptops": [
        ("CloudLite Pro 14", "Ultra-thin laptop for coding and productivity. 16GB RAM, 512GB SSD, Intel i7.", 64999, {"RAM": "16GB", "Storage": "512GB SSD", "Processor": "Intel i7"}),
        ("GameStorm X1", "High-performance gaming laptop with RTX 4060. 32GB RAM, 1TB SSD.", 124999, {"RAM": "32GB", "Storage": "1TB SSD", "GPU": "RTX 4060"}),
        ("EduBook 11", "Affordable student laptop. 8GB RAM, 256GB SSD, lightweight.", 29999, {"RAM": "8GB", "Storage": "256GB SSD", "Weight": "1.2kg"}),
        ("WorkForce 15", "Business laptop with fingerprint reader. 16GB RAM, 512GB SSD.", 74999, {"RAM": "16GB", "Storage": "512GB SSD", "Security": "Fingerprint"}),
        ("CreatorVision 16", "Content creation laptop with 4K OLED display.", 149999, {"RAM": "32GB", "Display": "4K OLED", "GPU": "RTX 4070"}),
        ("MacBook Air M3", "Latest Apple Silicon laptop. 8-core CPU, 10-core GPU, 16GB Unified Memory, 512GB SSD.", 114999, {"RAM": "16GB", "Storage": "512GB SSD", "Processor": "M3 Chip"}),
        ("ThinkPad X1 Carbon", "Premium business ultrabook. Intel Core Ultra 7, 32GB RAM, 1TB SSD.", 159999, {"RAM": "32GB", "Storage": "1TB SSD", "Processor": "Intel Core Ultra 7"}),
    ],
    "Smartphones": [
        ("NexaPhone Ultra", "Flagship smartphone with 200MP camera and 5000mAh battery.", 89999, {"Camera": "200MP", "Battery": "5000mAh"}),
        ("BudgetBuzz A5", "Best value smartphone under 15000. Great battery life.", 12999, {"Camera": "48MP", "Battery": "6000mAh"}),
        ("PixelSnap Pro", "Photography-focused phone with AI-enhanced camera system.", 54999, {"Camera": "108MP AI", "Storage": "256GB"}),
        ("SlimLine S22", "Ultra-slim design with AMOLED display.", 34999, {"Display": "AMOLED", "Weight": "155g"}),
        ("iPhone 15 Pro", "Titanium design with A17 Pro chip and 48MP main camera.", 134900, {"Camera": "48MP", "Processor": "A17 Pro", "Material": "Titanium"}),
        ("Samsung Galaxy S24 Ultra", "AI-powered flagship with S-Pen, 200MP camera, and Snapdragon 8 Gen 3.", 129999, {"Camera": "200MP", "Processor": "Snapdragon 8 Gen 3", "Feature": "S-Pen"}),
    ],
    "Tablets": [
        ("DrawPad 12", "Tablet for digital artists with stylus support.", 44999, {"Display": "12 inch", "Stylus": "Included"}),
        ("StreamTab 10", "Entertainment tablet with Dolby Atmos speakers.", 24999, {"Display": "10.5 inch", "Audio": "Dolby Atmos"}),
    ],
    "Headphones": [
        ("BassDrop Pro", "Over-ear noise-cancelling headphones with 40hr battery.", 7999, {"Type": "Over-ear", "ANC": "Yes", "Battery": "40hr"}),
        ("AirBuds Lite", "True wireless earbuds with transparency mode.", 3499, {"Type": "TWS", "Battery": "8hr"}),
        ("StudioMix 7", "Professional studio monitoring headphones.", 12999, {"Type": "Over-ear", "Driver": "50mm"}),
    ],
    "Cameras": [
        ("SnapShot DSLR 3000", "Entry-level DSLR with 24MP sensor and kit lens.", 39999, {"Sensor": "24MP APS-C", "Lens": "18-55mm kit"}),
        ("MirrorFlex Z5", "Mirrorless camera with 4K video and fast autofocus.", 89999, {"Sensor": "45MP Full Frame", "Video": "4K 60fps"}),
    ],
    "Men's Clothing": [
        ("Classic Oxford Shirt", "100% cotton formal shirt in navy blue.", 1499, {"Material": "Cotton", "Fit": "Regular"}),
        ("Urban Joggers", "Comfortable jogger pants for daily wear.", 999, {"Material": "Cotton blend", "Fit": "Relaxed"}),
        ("Premium Blazer", "Slim-fit blazer for formal occasions.", 4999, {"Material": "Polyester blend", "Fit": "Slim"}),
    ],
    "Women's Clothing": [
        ("Floral Maxi Dress", "Elegant floral print maxi dress for summer.", 1999, {"Material": "Rayon", "Length": "Maxi"}),
        ("Power Suit Set", "Professional 2-piece suit set.", 5999, {"Material": "Polyester", "Pieces": "2"}),
        ("Casual Denim Jacket", "Classic denim jacket with button closure.", 2499, {"Material": "Denim", "Fit": "Regular"}),
        ("Velvet Evening Gown", "Luxurious velvet gown for parties and formal events.", 3499, {"Material": "Velvet", "Length": "Floor length"}),
        ("Boho Summer Midi Dress", "Lightweight bohemian style midi dress.", 1599, {"Material": "Cotton Blend", "Length": "Midi"}),
    ],
    "Makeup": [
        ("Velvet Matte Lipstick", "Long-lasting matte lipstick in Ruby Red.", 599, {"Finish": "Matte", "Shade": "Ruby Red"}),
        ("Flawless Finish Foundation", "24-hour wear liquid foundation with SPF 15.", 1299, {"Coverage": "Full", "SPF": "15"}),
        ("Luminous Glow Highlighter", "Liquid highlighter drops for a radiant glow.", 899, {"Type": "Liquid", "Finish": "Radiant"}),
        ("Pro Eyeshadow Palette", "18 highly pigmented warm and neutral shades.", 2499, {"Shades": "18", "Finish": "Mixed"}),
        ("Waterproof Volumizing Mascara", "Intense black mascara for thick, long lashes.", 749, {"Feature": "Waterproof", "Color": "Black"}),
    ],
    "Shoes": [
        ("RunFast 3.0", "Lightweight running shoes with cushioned sole.", 3999, {"Type": "Running", "Weight": "220g"}),
        ("UrbanStep Sneakers", "Trendy casual sneakers.", 2499, {"Type": "Casual", "Sole": "Rubber"}),
        ("Formal Oxford", "Classic leather oxford shoes.", 4999, {"Type": "Formal", "Material": "Genuine Leather"}),
    ],
    "Accessories": [
        ("Leather Wallet", "Genuine leather bifold wallet.", 799, {"Material": "Leather", "Type": "Bifold"}),
        ("Aviator Sunglasses", "UV400 polarized aviator sunglasses.", 1299, {"UV": "400", "Type": "Aviator"}),
    ],
    "Furniture": [
        ("ErgoDesk Pro", "Height-adjustable standing desk with cable management.", 14999, {"Type": "Standing Desk", "Motor": "Dual"}),
        ("CloudSoft Sofa", "3-seater fabric sofa with memory foam cushions.", 24999, {"Seats": "3", "Material": "Fabric"}),
    ],
    "Cookware": [
        ("ChefMaster Pan Set", "5-piece non-stick cookware set.", 3999, {"Pieces": "5", "Coating": "Non-stick"}),
        ("Cast Iron Skillet", "Pre-seasoned cast iron skillet 12 inch.", 1999, {"Material": "Cast Iron", "Size": "12 inch"}),
    ],
    "Decor": [
        ("Minimalist Wall Clock", "Wooden wall clock with silent mechanism.", 899, {"Material": "Wood", "Mechanism": "Silent"}),
        ("LED Fairy Lights", "20ft warm white LED string lights.", 499, {"Length": "20ft", "Color": "Warm White"}),
    ],
    "Appliances": [
        ("TurboBlend 500", "High-speed blender with 5 presets.", 4999, {"Power": "500W", "Presets": "5"}),
        ("AirPure 360", "HEPA air purifier for rooms up to 500 sq ft.", 9999, {"Filter": "HEPA", "Coverage": "500 sq ft"}),
    ],
    "Fiction": [
        ("The Silent Echo", "A gripping thriller set in the Himalayas.", 399, {"Pages": "320", "Genre": "Thriller"}),
        ("Monsoon Dreams", "A heartwarming story of family and love.", 299, {"Pages": "280", "Genre": "Literary Fiction"}),
    ],
    "Non-Fiction": [
        ("Code & Conquer", "A guide to mastering software engineering interviews.", 599, {"Pages": "450", "Genre": "Technology"}),
        ("Mind Over Market", "Behavioral economics for everyday decisions.", 499, {"Pages": "380", "Genre": "Economics"}),
    ],
    "Academic": [
        ("Data Structures in Python", "Comprehensive textbook for CS students.", 799, {"Pages": "600", "Level": "Undergraduate"}),
        ("Linear Algebra Done Right", "Clear and rigorous linear algebra textbook.", 699, {"Pages": "340", "Level": "Undergraduate"}),
    ],
    "Comics": [
        ("Cyber Samurai Vol 1", "Sci-fi manga set in Neo-Tokyo 2084.", 199, {"Pages": "200", "Genre": "Sci-Fi Manga"}),
    ],
    "Yoga": [
        ("ZenMat Premium", "Extra thick 6mm yoga mat with alignment lines.", 1299, {"Thickness": "6mm", "Material": "TPE"}),
        ("Yoga Block Set", "Set of 2 high-density foam yoga blocks.", 599, {"Pieces": "2", "Material": "Foam"}),
        ("AeroFit Yoga Pants", "High-waist seamless leggings for yoga and workouts.", 1499, {"Material": "Spandex/Nylon", "Fit": "High-waist"}),
    ],
    "Fitness": [
        ("PowerGrip Dumbbells 5kg", "Pair of rubber-coated hex dumbbells.", 1499, {"Weight": "5kg pair", "Coating": "Rubber"}),
        ("Resistance Band Set", "Set of 5 resistance bands with handles.", 799, {"Bands": "5", "Resistance": "10-50 lbs"}),
        ("Pro Whey Protein", "100% Whey Protein Isolate, Double Rich Chocolate, 2kg.", 4999, {"Weight": "2kg", "Flavor": "Chocolate"}),
        ("Steel Shaker Bottle", "Insulated stainless steel shaker bottle 750ml.", 899, {"Capacity": "750ml", "Material": "Stainless Steel"}),
    ],
    "Outdoor": [
        ("TrekMaster Backpack 50L", "Waterproof hiking backpack with rain cover.", 3499, {"Capacity": "50L", "Waterproof": "Yes"}),
        ("CampEase Tent 4P", "4-person dome tent with easy setup.", 5999, {"Capacity": "4 Person", "Setup": "Quick pitch"}),
        ("TrailBlazer Hiking Boots", "Waterproof hiking boots with superior grip.", 4599, {"Type": "Boots", "Feature": "Waterproof"}),
    ],
    "Team Sports": [
        ("ProKick Football", "FIFA-approved match football size 5.", 1499, {"Size": "5", "Approval": "FIFA"}),
        ("SwiftHit Cricket Bat", "English willow cricket bat grade 2.", 4999, {"Material": "English Willow", "Grade": "2"}),
        ("SlamDunk Basketball", "Indoor/Outdoor composite leather basketball size 7.", 1299, {"Size": "7", "Material": "Composite Leather"}),
    ],
}

BRANDS = [
    "NexaTech", "SwiftGear", "EcoLine", "UrbanEdge", "PrimeCraft",
    "Zenith", "VeloCity", "ApexDrive", "NovaWear", "PureForm",
]


def create_categories():
    print("Creating categories...")
    created = {}
    for parent_name, children in CATEGORIES.items():
        parent_slug = slugify(parent_name)
        parent, _ = Category.objects.get_or_create(name=parent_name, slug=parent_slug)
        created[parent_name] = parent
        for child_name in children:
            child_slug = slugify(child_name)
            child, _ = Category.objects.get_or_create(name=child_name, slug=child_slug, parent=parent)
            created[child_name] = child
    print(f"  → {len(created)} categories ready")
    return created


def create_tags():
    print("Creating tags...")
    tag_objects = {}
    for tag_name in TAGS:
        tag, _ = ProductTag.objects.get_or_create(name=tag_name, slug=slugify(tag_name))
        tag_objects[tag_name] = tag
    print(f"  → {len(tag_objects)} tags ready")
    return tag_objects


def create_products(categories, tags):
    print("Creating products...")
    count = 0
    all_products = []
    for subcat_name, items in PRODUCTS.items():
        category = categories.get(subcat_name)
        if not category:
            continue
        for name, desc, price, specs in items:
            slug = slugify(name)
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": desc,
                    "category": category,
                    "brand": random.choice(BRANDS),
                    "price": Decimal(str(price)),
                    "discount_percent": Decimal(str(random.choice([0, 5, 10, 15, 20]))),
                    "stock": random.randint(5, 200),
                    "specs": specs,
                    "rating": Decimal(str(round(random.uniform(3.0, 5.0), 2))),
                }
            )
            if created:
                # Assign 2-4 random tags
                product.tags.set(random.sample(list(tags.values()), k=random.randint(2, 4)))
                count += 1
            all_products.append(product)
    print(f"  → {count} products created ({len(all_products)} total)")
    return all_products


def create_users():
    print("Creating test users...")
    users = []
    names = [
        ("anu", "anu@example.com"), ("ravi", "ravi@example.com"),
        ("priya", "priya@example.com"), ("arjun", "arjun@example.com"),
        ("meera", "meera@example.com"), ("kiran", "kiran@example.com"),
        ("dev", "dev@example.com"), ("neha", "neha@example.com"),
        ("sahil", "sahil@example.com"), ("anita", "anita@example.com"),
    ]
    for username, email in names:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "role": User.Role.CUSTOMER}
        )
        if created:
            user.set_password("Test@1234")
            user.save()
        users.append(user)
    
    # Create admin
    admin, created = User.objects.get_or_create(
        username="admin",
        defaults={"email": "admin@nexacart.com", "role": User.Role.ADMIN, "is_staff": True, "is_superuser": True}
    )
    if created:
        admin.set_password("Admin@1234")
        admin.save()
    
    print(f"  → {len(users)} customers + 1 admin ready")
    return users


def generate_interactions(users, products):
    print("Generating synthetic interactions...")
    interaction_types = list(Interaction.InteractionType.values)
    weights = [50, 15, 10, 10, 5, 10]  # VIEW heavy, PURCHASE rare
    count = 0
    
    for user in users:
        # Each user gets 20-80 random interactions
        num_interactions = random.randint(20, 80)
        # Bias towards a few "preferred" categories for realistic clustering
        preferred_products = random.sample(products, k=min(15, len(products)))
        
        for _ in range(num_interactions):
            # 70% chance to interact with preferred products, 30% random
            if random.random() < 0.7:
                product = random.choice(preferred_products)
            else:
                product = random.choice(products)
            
            itype = random.choices(interaction_types, weights=weights, k=1)[0]
            Interaction.objects.create(
                user=user,
                product=product,
                interaction_type=itype,
                metadata={"source": "synthetic_generator"}
            )
            count += 1
    
    print(f"  → {count} interactions generated")


def generate_orders(users, products):
    print("Generating synthetic orders...")
    count = 0
    statuses = [
        Order.OrderStatus.DELIVERED, Order.OrderStatus.SHIPPED,
        Order.OrderStatus.PROCESSING, Order.OrderStatus.PLACED,
    ]
    
    for user in users:
        num_orders = random.randint(1, 5)
        for _ in range(num_orders):
            order = Order.objects.create(
                user=user,
                shipping_address_snapshot="123 Test Street, Mumbai, MH 400001",
                status=random.choice(statuses),
                total_amount=Decimal("0.00")
            )
            total = Decimal("0.00")
            num_items = random.randint(1, 4)
            chosen = random.sample(products, k=min(num_items, len(products)))
            for product in chosen:
                qty = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price_at_time_of_purchase=product.price
                )
                total += product.price * qty
            order.total_amount = total
            order.save()
            count += 1
    
    print(f"  → {count} orders generated")


if __name__ == "__main__":
    print("=" * 50)
    print("NexaCart Synthetic Data Generator")
    print("=" * 50)
    categories = create_categories()
    tags = create_tags()
    products = create_products(categories, tags)
    users = create_users()
    generate_interactions(users, products)
    generate_orders(users, products)
    print("=" * 50)
    print("✓ Seed data generation complete!")
    print(f"  Products: {Product.objects.count()}")
    print(f"  Users: {User.objects.count()}")
    print(f"  Interactions: {Interaction.objects.count()}")
    print(f"  Orders: {Order.objects.count()}")
    print("=" * 50)
