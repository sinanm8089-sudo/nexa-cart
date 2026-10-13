"""
Generate ~1,000 realistic e-commerce products for NexaCart,
with a substantial, rich collection of Makeup, Beauty, Cosmetics, Skincare,
along with Electronics, Fashion, Home & Living, and Fitness items.
Also seeds corresponding realistic customer reviews across the new products.
"""
import os
import sys
import random
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
import django
django.setup()

from django.utils.text import slugify
from products.models import Category, Product, ProductTag
from reviews.models import Review
from accounts.models import User

# ── 1. EXPANDED CATEGORY HIERARCHY ───────────────────────────────
CATEGORY_TREE = {
    "Beauty & Personal Care": [
        "Makeup", "Skincare", "Fragrances", "Haircare", "Beauty Tools"
    ],
    "Electronics": [
        "Laptops", "Smartphones", "Audio & Headphones", "Wearables & Smartwatches",
        "Cameras & Photography", "Gaming & Accessories", "PC Peripherals"
    ],
    "Fashion & Apparel": [
        "Women's Clothing", "Men's Clothing", "Footwear", "Bags & Luggage", "Jewellery & Watches"
    ],
    "Home & Kitchen": [
        "Kitchen Appliances", "Cookware & Dining", "Home Decor", "Furniture", "Smart Home"
    ],
    "Sports & Fitness": [
        "Gym Equipment", "Yoga & Pilates", "Nutrition & Supplements", "Outdoor & Camping"
    ],
    "Books & Media": [
        "Fiction", "Self-Help & Business", "Technology & Coding", "Comics & Manga"
    ]
}

# ── 2. BRANDS PER DOMAIN ──────────────────────────────────────────
BEAUTY_BRANDS = [
    "M.A.C Cosmetics", "Maybelline New York", "L'Oréal Paris", "Nykaa Cosmetics",
    "Lakmé", "Sugar Cosmetics", "Rare Beauty", "Charlotte Tilbury", "Fenty Beauty",
    "Huda Beauty", "The Ordinary", "Minimalist", "Cetaphil", "Dot & Key",
    "Forest Essentials", "Kama Ayurveda", "Colorbar", "Plum Goodness", "Laneige"
]

TECH_BRANDS = [
    "Apple", "Samsung", "Sony", "Dell", "HP", "Asus ROG", "Lenovo", "OnePlus",
    "Bose", "Sennheiser", "Logitech", "Anker", "Nothing", "Xiaomi", "Google", "Boat", "JBL"
]

FASHION_BRANDS = [
    "Zara", "H&M", "Nike", "Adidas", "Puma", "Levi's", "Tommy Hilfiger",
    "Calvin Klein", "Allen Solly", "Fabindia", "Mango", "Vero Moda", "Ray-Ban"
]

HOME_BRANDS = [
    "Philips", "Dyson", "Prestige", "Wonderchef", "IKEA", "Nespresso",
    "Morphy Richards", "Bajaj", "SleepyCat", "Solimo", "Pigeon"
]

FITNESS_BRANDS = [
    "Decathlon", "MuscleBlaze", "Optimum Nutrition", "Boldfit", "Yonex", "Cultsport", "Reebok"
]

BOOK_PUBLISHERS = [
    "Penguin Random House", "HarperCollins", "O'Reilly Media", "Bloomsbury", "Simon & Schuster"
]

# ── 3. PRODUCT CATALOG BLUEPRINTS ─────────────────────────────────

# --- A. MAKEUP & BEAUTY BLUEPRINTS (Extensive!) ---
MAKEUP_BLUEPRINTS = [
    # Lipsticks & Lip Care
    ("Matte As Hell Crayon Lipstick", "Sugar Cosmetics", 799, "Lipstick", {"Finish": "Silky Matte", "Wear": "12hr Long-Wear", "Shade": "Scarlett O'Hara"}),
    ("Powder Kiss Velvet Blur Slim Stick", "M.A.C Cosmetics", 2450, "Lipstick", {"Finish": "Soft-focus Matte", "Weight": "2g", "Shade": "Devoted To Chili"}),
    ("SuperStay Vinyl Ink Liquid Lipstick", "Maybelline New York", 849, "Lipstick", {"Finish": "Instant Vinyl Shine", "Wear": "16hr No-Transfer", "Shade": "Cheeky"}),
    ("Rouge Signature Matte Liquid Ink", "L'Oréal Paris", 699, "Lipstick", {"Finish": "Ultra-light Matte", "Formula": "Water-infused", "Shade": "I Empower"}),
    ("Soft Pinch Tinted Lip Oil", "Rare Beauty", 2400, "Lip Care", {"Finish": "High-shine Jelly", "Nourishing": "Jojoba & Sunflower Seed", "Shade": "Joy"}),
    ("Pillow Talk Matte Revolution Lipstick", "Charlotte Tilbury", 3400, "Lipstick", {"Finish": "Luminous Modern-Matte", "Enriched": "Lipstick Tree extract", "Shade": "Pillow Talk Original"}),
    ("Ultra Matte Liquid Lip Color", "Nykaa Cosmetics", 499, "Lipstick", {"Finish": "Transferproof Matte", "Shade": "Chai", "CrueltyFree": "Yes"}),
    ("Gloss Bomb Universal Lip Luminizer", "Fenty Beauty", 2150, "Lip Gloss", {"Finish": "Shimmer Shine", "Scent": "Peach-Vanilla", "Shade": "Fenty Glow"}),
    ("Forever Matte Liquid Lip Color", "Lakmé", 349, "Lipstick", {"Finish": "Intense Matte", "Wear": "16hr", "Shade": "Red Carpet"}),
    ("Lip Sleeping Mask Berry", "Laneige", 1350, "Lip Care", {"Benefit": "Deep Overnight Hydration", "KeyIngredient": "Berry Fruit Complex", "Size": "20g"}),
    
    # Foundations & Complexion
    ("Fit Me Matte + Poreless Liquid Foundation", "Maybelline New York", 629, "Foundation", {"Coverage": "Medium-to-Full", "Finish": "Natural Matte", "SPF": "22", "Shade": "128 Warm Nude"}),
    ("Studio Fix Fluid Foundation SPF 15", "Studio Fix", 3600, "Foundation", {"Coverage": "Full", "Finish": "Natural Matte", "SPF": "15", "Control": "24hr Oil-Control"}),
    ("True Match Nude Plumping Tinted Serum", "L'Oréal Paris", 1199, "Complexion", {"KeyIngredient": "1% Pure Hyaluronic Acid", "Finish": "Dewy Luminous", "Coverage": "Sheer-to-Medium"}),
    ("Airbrush Flawless Longwear Foundation", "Charlotte Tilbury", 4600, "Foundation", {"Coverage": "Full Coverage", "Technology": "Anti-Pollution Magic", "Finish": "Natural Soft Matte"}),
    ("Liquid Touch Weightless Foundation", "Rare Beauty", 3200, "Foundation", {"Coverage": "Medium Buildable", "Finish": "Skin-like", "Feature": "Breathable Botanical blend"}),
    ("9 to 5 Complexion Care CC Cream", "Lakmé", 360, "CC Cream", {"Coverage": "Daily Sheer", "SPF": "30 PA++", "SkinType": "All Skin Types"}),
    ("Skin Serum Foundation with Vitamin C", "Nykaa Cosmetics", 899, "Foundation", {"Finish": "Radiant Dewy", "Benefit": "Antioxidant Brightening", "SPF": "15"}),
    ("Pro Filt'r Soft Matte Longwear Foundation", "Fenty Beauty", 3900, "Foundation", {"Finish": "Soft Matte", "ClimateAdaptive": "Sweat & Shine Resistant", "Shades": "50 Shades Available"}),
    
    # Eyes & Brows
    ("Lash Sensational Sky High Waterproof Mascara", "Maybelline New York", 799, "Mascara", {"Formula": "Bamboo Extract & Fibers", "Effect": "Limitless Length", "Feature": "Waterproof"}),
    ("Voluminous Lash Paradise Mascara", "L'Oréal Paris", 849, "Mascara", {"Effect": "Feathery Soft Volume", "Formula": "Castor Oil Enriched", "Color": "Carbon Black"}),
    ("Eyeconic Liquid Waterproof Eyeliner", "Lakmé", 260, "Eyeliner", {"Finish": "Deep Matte Black", "Wear": "24hr Smudge-proof", "Tip": "Precision Flexible Brush"}),
    ("Born This Way The Natural Nudes Eye Palette", "Huda Beauty", 4950, "Eyeshadow", {"Pans": "16 Multi-Finish Shades", "Texture": "Creamy Velvet", "Finish": "Matte & Metallic Shimmer"}),
    ("Epic Ink Waterproof Vegan Eyeliner", "Nykaa Cosmetics", 599, "Eyeliner", {"Tip": "0.1mm Micro Felt Tip", "Wear": "Waterproof & Transfer-proof"}),
    ("Arch Arrival Brow Definer Pencil", "Sugar Cosmetics", 499, "Brows", {"Shape": "Triangle Spoolie Applicator", "Wear": "12hr Sweat-proof", "Shade": "Taupe Tom"}),
    ("Empowered Luxury Eyeshadow Palette", "Huda Beauty", 5800, "Eyeshadow", {"Pans": "18 Pigmented Shades", "Formulas": "Gel Hybrid, Flakes & Wet Metals"}),
    
    # Cheeks, Blush & Highlighter
    ("Soft Pinch Liquid Blush", "Rare Beauty", 2500, "Blush", {"Formula": "Weightless Long-Lasting", "Finish": "Dewy Luminous", "Shade": "Hope (Nude Mauve)"}),
    ("Cheek Heat Sheer Gel-Cream Blush", "Maybelline New York", 499, "Blush", {"Formula": "Oil-Free Water Gel", "Finish": "Natural Flushed Glow"}),
    ("Mineralize Skinfinish Lightscapade Highlighter", "M.A.C Cosmetics", 3950, "Highlighter", {"Finish": "Multi-dimensional Frost", "Bake": "77-Mineral Complex"}),
    ("Contour De Force Mini Bronzer", "Sugar Cosmetics", 449, "Bronzer", {"Finish": "Matte Sun-kissed", "Shade": "01 Taupe Topper"}),
    ("Glowgasm Beauty Light Wand Highlighter", "Charlotte Tilbury", 4000, "Highlighter", {"Formula": "Luminous Gel Pigment", "Applicator": "Cushion Pad", "Shade": "Pinkgasm"}),
    ("Matte Real Setting Powder 16hr", "L'Oréal Paris", 799, "Powder", {"Effect": "Pore Blurring", "Wear": "16hr Shine Control"}),
    
    # Skincare Heroes
    ("Niacinamide 10% + Zinc 1% Blemish Serum", "The Ordinary", 600, "Serum", {"Active": "10% Niacinamide, 1% Zinc PCA", "Volume": "30ml", "SkinType": "Oily & Acne Prone"}),
    ("10% Vitamin C Face Serum for Glow", "Minimalist", 699, "Serum", {"Active": "Ethyl Ascorbic Acid + Centella", "Volume": "30ml", "SkinType": "All Skin Types"}),
    ("Gentle Skin Cleanser for Sensitive Skin", "Cetaphil", 399, "Cleanser", {"Formula": "Soap-free, Fragrance-free", "SkinBenefit": "Preserves Moisture Barrier", "Size": "125ml"}),
    ("Watermelon Glow Niacinamide Dew Drops", "Dot & Key", 795, "Serum", {"Finish": "Instant Glass Skin Glow", "KeyIngredients": "Hyaluronic Acid & Watermelon"}),
    ("Ceramide & Hyaluronic Barrier Repair Cream", "Minimalist", 599, "Moisturizer", {"Ceramides": "0.3% Pure Ceramides + Bisabolol", "SkinType": "Dry & Sensitive"}),
    ("Squalane Cleanser Hydrating Balm", "The Ordinary", 850, "Cleanser", {"Texture": "Balm-to-Oil-to-Milk", "Benefit": "Makeup Dissolving", "Volume": "50ml"}),
    ("Cica + Salicylic Acid Night Gel for Acne", "Dot & Key", 545, "Night Cream", {"Actives": "2% Salicylic Acid + Cica Extract", "Target": "Active Acne & Redness"}),
    ("Soundarya Radiance Cream with 24K Gold", "Forest Essentials", 6200, "Luxury Cream", {"Infusion": "24 Karat Pure Gold Bhasma & Saffron", "Volume": "50g"}),
    ("Kumkumadi Miraculous Ayurvedic Night Serum", "Kama Ayurveda", 3495, "Ayurvedic Oil", {"Herbs": "Pure Kashmiri Saffron & 26 Ayurvedic Herbs", "Volume": "12ml"}),
    ("Waterproof Invisible Matte Sunscreen SPF 50+", "Dot & Key", 495, "Sunscreen", {"Protection": "Broad Spectrum SPF 50 PA++++", "WhiteCast": "Zero White Cast"}),
    
    # Fragrances & Haircare
    ("Oud & Green Tea Luxury Eau De Parfum", "Forest Essentials", 4800, "Fragrance", {"Notes": "Fresh Green Tea, Cardamom & Warm Agarwood", "Size": "50ml"}),
    ("Kayali Vanilla | 28 Eau De Parfum", "Huda Beauty", 7600, "Fragrance", {"Notes": "Madagascar Vanilla, Jasmine, Tonka & Brown Sugar", "Size": "50ml"}),
    ("Rosemary & Biotin Anti-Hairfall Shampoo", "Plum Goodness", 399, "Haircare", {"Benefit": "Strengthens Hair Roots", "SulphateFree": "Yes", "Size": "250ml"}),
    ("No. 3 Hair Perfector Repair Treatment", "L'Oréal Paris", 2800, "Haircare", {"Technology": "Bond Building Complex", "Benefit": "Repairs Damaged & Colored Hair"}),
    ("Professional 24-Piece Rose Gold Brush Set", "Nykaa Cosmetics", 2299, "Tools", {"Bristles": "Cruelty-free Synthetic Taklon", "Bag": "Vegan Leather Roll"}),
]

# Variations generator for Makeup to scale up to 350+ beauty products
MAKEUP_TYPES = [
    ("Liquid Velvet Matte Lipstick", ["Ruby Scarlet", "Nude Mocha", "Plum Wine", "Cinnamon Toast", "Rose Petal", "Berry Crush", "Coral Peach", "Espresso Bliss"], [549, 699, 899, 1199]),
    ("Silk Satin Moisture Lipstick", ["Nude Honey", "Crimson Diva", "Peachy Keen", "Vintage Rose", "Cherry Bomb", "Warm Caramel"], [499, 649, 799, 999]),
    ("24hr Waterproof Precision Gel Eyeliner", ["Deep Carbon Black", "Metallic Bronze", "Emerald Green", "Sapphire Navy", "Chocolate Brown"], [349, 449, 599, 749]),
    ("Full Coverage Lightweight Concealer", ["Fair Ivory", "Light Beige", "Medium Sand", "Golden Honey", "Warm Tan", "Deep Caramel"], [499, 699, 899, 1299]),
    ("Radiant Glow Skin Tint Foundation SPF 30", ["Porcelain", "Ivory Warm", "Natural Buff", "Sun Beige", "Toffee"], [799, 999, 1299, 1899]),
    ("Hydrating Lip Glow Oil with Vitamin E", ["Berry Glaze", "Watermelon Popsicle", "Honey Drip", "Clear Crystal", "Rosy Quartz"], [399, 549, 699, 899]),
    ("Baked Marble Highlighter & Bronzer", ["Champagne Gold", "Rose Gold Shimmer", "Sunlit Bronze", "Pearl Radiance"], [599, 799, 1099, 1499]),
    ("Ultra-Fine Loose Setting Powder", ["Translucent Fair", "Banana Glow", "Medium Deep"], [499, 699, 899]),
    ("12-Color Multi-Finish Eyeshadow Palette", ["Sunset Dunes", "Smokey Obsidian", "Rose Quartz Fantasy", "Electric Neon Pop"], [899, 1299, 1799, 2499]),
    ("Volumizing Micro-Fiber Lash Mascara", ["Intense Jet Black", "Soft Cocoa Brown", "Midnight Blue"], [499, 699, 899]),
    ("Ultra-Hydrating Face Mist with Hyaluronic Acid", ["Rose Water & Aloe", "Cucumber Mint", "Lavender Dew"], [399, 549, 699]),
    ("Gentle Exfoliating Facial Serum", ["AHA 10% + BHA 2%", "Lactic Acid 5%", "Glycolic Glow 8%"], [599, 749, 899]),
]

# --- B. ELECTRONICS BLUEPRINTS ---
TECH_MODELS = [
    ("AeroBook Slim 15", "Dell", [49999, 57999, 69999], {"RAM": "16GB", "SSD": "512GB", "Processor": "Intel Core i5"}),
    ("Titan Gaming Strix 16", "Asus ROG", [99999, 119999, 149999], {"GPU": "RTX 4060", "RAM": "32GB", "Display": "165Hz QHD"}),
    ("ZenBook Duo OLED", "Asus ROG", [114999, 134999], {"Screen": "Dual OLED", "Processor": "Intel Core Ultra 7"}),
    ("MacBook Pro M3 Max", "Apple", [199900, 249900], {"Chip": "M3 Max", "Memory": "36GB Unified", "Storage": "1TB SSD"}),
    ("Galaxy Tab S9 Ultra", "Samsung", [74999, 89999], {"Display": "14.6 inch AMOLED", "Stylus": "S-Pen Included"}),
    ("iPad Air 11-inch M2", "Apple", [59900, 69900], {"Chip": "Apple M2", "LiquidRetina": "11-inch"}),
    ("WH-1000XM5 Wireless Headphones", "Sony", [26990, 29990], {"ANC": "Industry-leading ANC", "Battery": "30 Hours"}),
    ("QuietComfort Ultra Earbuds", "Bose", [21900, 24900], {"Audio": "Immersive Spatial Audio", "Fit": "CustomTune"}),
    ("AirPods Pro 2nd Gen USB-C", "Apple", [20900, 23900], {"Chip": "H2 Chip", "Feature": "Adaptive Audio & Transparency"}),
    ("SoundLink Revolve+ II Bluetooth Speaker", "Bose", [19900, 22500], {"Sound": "360-degree True Omnidirectional"}),
    ("MX Master 3S Wireless Performance Mouse", "Logitech", [8495, 9995], {"Sensor": "8K DPI Any-surface", "Clicks": "Quiet Clicks"}),
    ("G915 TKL Wireless Mechanical Keyboard", "Logitech", [16995, 18995], {"Switches": "GL Tactile Low Profile", "Lighting": "LIGHTSYNC RGB"}),
    ("Galaxy Watch 6 Classic LTE", "Samsung", [32999, 36999], {"Bezel": "Rotating Physical Bezel", "Health": "ECG & Blood Pressure"}),
    ("Apple Watch Series 9 GPS", "Apple", [39900, 44900], {"Chip": "S9 SiP", "Gesture": "Double Tap Feature"}),
    ("Alpha 7 IV Full-Frame Mirrorless Camera", "Sony", [189990, 219990], {"Sensor": "33MP Exmor R CMOS", "Video": "4K 60p 10-bit"}),
    ("4K Ultra-Wide Curved Monitor 34-inch", "Dell", [42999, 49999], {"Panel": "IPS 144Hz", "Curvature": "1900R Curved"}),
]

# --- C. FASHION BLUEPRINTS ---
FASHION_TEMPLATES = [
    ("Tailored Structured Blazer", ["Navy Blue", "Charcoal Grey", "Olive Green", "Beige Sand"], [3999, 5499, 7999]),
    ("100% Giza Cotton Formal Shirt", ["Classic White", "Sky Blue", "French Blue", "Soft Pink"], [1899, 2499, 3299]),
    ("Raw Selvedge Denim Slim Fit Jeans", ["Indigo Dark Wash", "Vintage Blue", "Washed Charcoal"], [2499, 3499, 4499]),
    ("Merino Wool Crewneck Sweater", ["Black", "Burgundy", "Forest Green", "Oatmeal Heather"], [2999, 3999, 4999]),
    ("Pure Mulberry Silk Banarasi Saree", ["Royal Crimson Gold", "Peacock Blue", "Emerald Zari", "Mustard Gold"], [6999, 11999, 18999]),
    ("Handcrafted Full-Grain Leather Derby Shoes", ["Cognac Tan", "Midnight Black", "Oxblood Deep"], [4499, 5999, 7999]),
    ("Retro Air Jordan 1 Low Top Sneakers", ["Bred Toe", "Panda White/Black", "University Blue"], [7995, 9995, 12995]),
    ("Lightweight Seamless Performance Leggings", ["Smoky Mauve", "Jet Black", "Cobalt Blue"], [1499, 1999, 2499]),
    ("Minimalist Top-Grain Leather Tote Bag", ["Cognac Tan", "Charcoal Black", "Taupe Grey"], [3499, 4999, 6499]),
    ("Aviator Polarized Classic Sunglasses", ["Gold Frame / G-15 Green", "Gunmetal / Polarized Grey"], [6290, 8490]),
]

# --- D. HOME & KITCHEN BLUEPRINTS ---
HOME_TEMPLATES = [
    ("Dual Basket Digital Air Fryer 8.5L", "Philips", 11999, {"Capacity": "8.5 Litres", "Power": "2200W", "Presets": "8"}),
    ("V15 Detect Extra Cordless Vacuum", "Dyson", 59900, {"Laser": "Fluffy Optic Head", "Suction": "240 AW", "Runtime": "60 mins"}),
    ("Espresso Barista Touch Coffee Machine", "Nespresso", 28990, {"Pressure": "19 Bar High Pressure", "Milk": "Auto Frother Steam Wand"}),
    ("Hard Anodized 3-Piece Induction Pan Set", "Prestige", 3299, {"Material": "Hard Anodized Aluminum", "Pieces": "3"}),
    ("Tri-Ply Stainless Steel Dutch Oven with Lid", "Wonderchef", 2899, {"Capacity": "5 Litres", "Technology": "Tri-Ply Heat Distribution"}),
    ("Ergonomic Dual-Motor Motorized Standing Desk", "IKEA", 22999, {"HeightRange": "70cm - 120cm", "Memory": "4 Preset Slots"}),
    ("Orthopedic Memory Foam Mattress King 8-inch", "SleepyCat", 16999, {"Layers": "CoolTEC Gel Memory Foam", "Warranty": "10 Years"}),
    ("HEPA 4-Stage True Air Purifier with AQI Display", "Philips", 14999, {"Filter": "NanoProtect HEPA", "CADR": "380 m3/h"}),
    ("Smart LED WiFi Dimmable Ceiling Fixture 48W", "Philips", 4499, {"Color": "16 Million Colors RGB", "Compatibility": "Alexa & Google"}),
]

# --- E. FITNESS BLUEPRINTS ---
FITNESS_TEMPLATES = [
    ("Gold Standard 100% Whey Protein 2kg", "Optimum Nutrition", 6299, {"Protein": "24g per scoop", "BCAAs": "5.5g", "Flavor": "Double Rich Chocolate"}),
    ("Biozyme Performance Whey Protein 2kg", "MuscleBlaze", 4499, {"Absorption": "Enhanced Absorption Formula EAF", "Flavor": "Rich Milk Chocolate"}),
    ("Cast Iron Adjustable Hex Dumbbells 20kg Set", "Decathlon", 4999, {"Weight": "20kg Total", "Plates": "Rubber Encased Cast Iron"}),
    ("Astrox 99 Pro Tour Badminton Racket", "Yonex", 11490, {"Frame": "HM Graphite / Namd", "Balance": "Head Heavy", "String": "Unstrung"}),
    ("Non-Slip Natural Tree Rubber Yoga Mat 5mm", "Boldfit", 2199, {"Material": "Eco Natural Rubber", "Thickness": "5mm", "Grip": "Sweat Activated"}),
]

# --- F. BOOKS BLUEPRINTS ---
BOOK_TEMPLATES = [
    ("Designing Data-Intensive Applications", "O'Reilly Media", 1699, {"Author": "Martin Kleppmann", "Pages": "616", "Topic": "Distributed Systems"}),
    ("System Design Interview – An Insider's Guide", "Penguin Random House", 1499, {"Author": "Alex Xu", "Pages": "320", "Topic": "Software Architecture"}),
    ("Atomic Habits: An Easy & Proven Way to Build Good Habits", "Penguin Random House", 599, {"Author": "James Clear", "Pages": "320", "Genre": "Self-Improvement"}),
    ("Thinking, Fast and Slow", "Penguin Random House", 650, {"Author": "Daniel Kahneman", "Pages": "512", "Topic": "Cognitive Psychology"}),
    ("Clean Code: A Handbook of Agile Software Craftsmanship", "Pearson", 899, {"Author": "Robert C. Martin", "Pages": "464", "Topic": "Programming Best Practices"}),
]


def ensure_categories():
    """Create all primary categories and subcategories in the database."""
    print("Ensuring categories structure exists...")
    category_map = {}
    for parent_name, subs in CATEGORY_TREE.items():
        parent_slug = slugify(parent_name)
        parent, _ = Category.objects.get_or_create(
            slug=parent_slug,
            defaults={"name": parent_name, "description": f"All {parent_name} products"}
        )
        category_map[parent_name] = parent

        for sub_name in subs:
            sub_slug = slugify(f"{parent_name}-{sub_name}")
            sub, _ = Category.objects.get_or_create(
                slug=sub_slug,
                defaults={
                    "name": sub_name,
                    "parent": parent,
                    "description": f"{sub_name} under {parent_name}"
                }
            )
            category_map[sub_name] = sub

    return category_map


def generate_unique_slug(base_name, existing_slugs):
    base_slug = slugify(base_name)
    slug = base_slug
    counter = 1
    while slug in existing_slugs or Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    existing_slugs.add(slug)
    return slug


def populate_catalog():
    print("=" * 60)
    print("NexaCart ~1,000 Product Expansion Generator")
    print("=" * 60)

    category_map = ensure_categories()
    existing_slugs = set(Product.objects.values_list('slug', flat=True))
    current_count = Product.objects.count()
    print(f"Current catalog count: {current_count} products.")
    target_count = 1000
    needed_count = max(0, target_count - current_count)
    print(f"Generating {needed_count} new products to reach ~1,000 products...")

    products_to_create = []

    # -------------------------------------------------------------
    # 1. MAKEUP & BEAUTY COLLECTION (Target ~350 products)
    # -------------------------------------------------------------
    makeup_cat = category_map.get("Makeup")
    skincare_cat = category_map.get("Skincare")
    fragrance_cat = category_map.get("Fragrances")
    haircare_cat = category_map.get("Haircare")
    tools_cat = category_map.get("Beauty Tools")

    # Add direct makeup blueprints
    for name, brand, price, sub_type, specs in MAKEUP_BLUEPRINTS:
        if len(products_to_create) >= needed_count:
            break
        slug = generate_unique_slug(f"{brand} {name}", existing_slugs)
        target_category = makeup_cat
        if "Serum" in name or "Cream" in name or "Cleanser" in name or "Sunscreen" in name:
            target_category = skincare_cat
        elif "Parfum" in name or "Fragrance" in name:
            target_category = fragrance_cat
        elif "Hair" in name or "Shampoo" in name:
            target_category = haircare_cat
        elif "Brush" in name or "Tools" in name:
            target_category = tools_cat

        products_to_create.append(Product(
            name=f"{name}",
            slug=slug,
            category=target_category,
            brand=brand,
            price=Decimal(str(price)),
            discount_percent=Decimal(str(random.choice([0, 5, 10, 15, 20, 25]))),
            stock=random.randint(15, 250),
            specs=specs,
            rating=Decimal(str(round(random.uniform(3.7, 4.9), 2))),
            description=f"Authentic {brand} {name}. Dermatologically tested, high-performance cosmetic formulation offering radiant results and long-lasting wear."
        ))

    # Add variations across shades and finishes to reach ~350 beauty products
    for base_type, shades, prices in MAKEUP_TYPES:
        for brand in BEAUTY_BRANDS:
            if len(products_to_create) >= 380:
                break
            for shade in shades:
                if len(products_to_create) >= 380:
                    break
                price = random.choice(prices)
                prod_name = f"{brand} {base_type} - {shade}"
                slug = generate_unique_slug(prod_name, existing_slugs)
                specs = {
                    "Shade": shade,
                    "Brand": brand,
                    "CrueltyFree": "Yes",
                    "NetWeight": f"{random.choice([3.5, 4.2, 5.0, 30])}g/ml",
                    "Finish": "Matte" if "Matte" in base_type else ("Luminous" if "Glow" in base_type else "Natural")
                }
                products_to_create.append(Product(
                    name=prod_name,
                    slug=slug,
                    category=makeup_cat,
                    brand=brand,
                    price=Decimal(str(price)),
                    discount_percent=Decimal(str(random.choice([0, 5, 10, 15]))),
                    stock=random.randint(20, 300),
                    specs=specs,
                    rating=Decimal(str(round(random.uniform(3.8, 4.9), 2))),
                    description=f"{brand} {base_type} in {shade}. Ultra-pigmented formulation delivering saturated color payoff, non-drying comfort, and all-day confidence."
                ))

    print(f"Generated {len(products_to_create)} Beauty & Makeup products so far...")

    # -------------------------------------------------------------
    # 2. ELECTRONICS & COMPUTING (Target ~200 products)
    # -------------------------------------------------------------
    elec_cats = [
        category_map.get("Laptops"), category_map.get("Smartphones"),
        category_map.get("Audio & Headphones"), category_map.get("Wearables & Smartwatches"),
        category_map.get("Cameras & Photography"), category_map.get("Gaming & Accessories"),
        category_map.get("PC Peripherals")
    ]

    for model, brand, prices, specs in TECH_MODELS:
        for p_idx, price in enumerate(prices):
            variant_name = f"{brand} {model}" + (f" (Config {p_idx+1})" if len(prices) > 1 else "")
            slug = generate_unique_slug(variant_name, existing_slugs)
            cat_choice = elec_cats[0] if "Book" in model or "Gaming" in model else (
                elec_cats[1] if "Galaxy" in model or "Apple" in model and "Watch" not in model and "Mac" not in model else (
                    elec_cats[2] if "Headphones" in model or "Earbuds" in model or "Speaker" in model else (
                        elec_cats[3] if "Watch" in model else (
                            elec_cats[4] if "Camera" in model else elec_cats[6]
                        )
                    )
                )
            )

            products_to_create.append(Product(
                name=variant_name,
                slug=slug,
                category=cat_choice,
                brand=brand,
                price=Decimal(str(price)),
                discount_percent=Decimal(str(random.choice([0, 5, 8, 12]))),
                stock=random.randint(5, 80),
                specs=specs,
                rating=Decimal(str(round(random.uniform(3.9, 4.9), 2))),
                description=f"Official {brand} {variant_name}. Engineered for premium performance, unmatched build quality, and cutting-edge productivity."
            ))

    # Tech variation generators
    tech_variants = [
        ("Pro Wireless ANC Earbuds V", TECH_BRANDS, [2999, 4499, 7999, 12999], category_map.get("Audio & Headphones"), {"ANC": "Up to 35dB", "Battery": "36hr Total"}),
        ("Fast Charge Power Bank 20000mAh", TECH_BRANDS, [1499, 1999, 2799], category_map.get("PC Peripherals"), {"Capacity": "20,000mAh", "Output": "65W USB-C PD"}),
        ("Mechanical RGB Gaming Keyboard Pro", TECH_BRANDS, [3499, 5999, 8999], category_map.get("Gaming & Accessories"), {"Switches": "Hot-swappable Mechanical", "RGB": "Per-key"}),
        ("Precision Ergonomic Wireless Mouse", TECH_BRANDS, [1299, 2499, 4999], category_map.get("PC Peripherals"), {"DPI": "4000 DPI Sensor", "Connectivity": "Bluetooth + 2.4GHz"}),
        ("Ultra-Slim AMOLED Smartwatch 1.43", TECH_BRANDS, [3999, 6999, 12999], category_map.get("Wearables & Smartwatches"), {"Display": "AMOLED Always-On", "Sensors": "Heart Rate & SpO2"}),
        ("4K 60fps Creator Webcam with Ring Light", TECH_BRANDS, [2999, 4999, 7999], category_map.get("PC Peripherals"), {"Resolution": "4K Ultra HD", "Microphone": "Dual Noise Cancelling"}),
    ]

    for template, brands, prices, cat, base_specs in tech_variants:
        for brand in brands:
            if len(products_to_create) >= 550:
                break
            for v_num in [1, 2]:
                price = random.choice(prices)
                pname = f"{brand} {template}{v_num}"
                slug = generate_unique_slug(pname, existing_slugs)
                specs = dict(base_specs)
                specs["ModelYear"] = "2026"
                products_to_create.append(Product(
                    name=pname,
                    slug=slug,
                    category=cat,
                    brand=brand,
                    price=Decimal(str(price)),
                    discount_percent=Decimal(str(random.choice([0, 5, 10, 15]))),
                    stock=random.randint(15, 120),
                    specs=specs,
                    rating=Decimal(str(round(random.uniform(3.8, 4.8), 2))),
                    description=f"{pname} brings next-gen speed, reliability, and modern aesthetic to your everyday digital workflow."
                ))

    print(f"Generated {len(products_to_create)} total products (including Tech)...")

    # -------------------------------------------------------------
    # 3. FASHION & APPAREL (Target ~200 products)
    # -------------------------------------------------------------
    fashion_cats = [
        category_map.get("Men's Clothing"), category_map.get("Women's Clothing"),
        category_map.get("Footwear"), category_map.get("Bags & Luggage"),
        category_map.get("Jewellery & Watches")
    ]

    for item_base, colors, prices in FASHION_TEMPLATES:
        for brand in FASHION_BRANDS:
            if len(products_to_create) >= 750:
                break
            for color in colors[:2]:
                if len(products_to_create) >= 750:
                    break
                price = random.choice(prices)
                pname = f"{brand} {item_base} ({color})"
                slug = generate_unique_slug(pname, existing_slugs)
                cat = fashion_cats[2] if "Shoes" in item_base or "Sneakers" in item_base else (
                    fashion_cats[3] if "Bag" in item_base else (
                        fashion_cats[4] if "Sunglasses" in item_base or "Saree" in item_base else fashion_cats[0]
                    )
                )
                specs = {"Color": color, "Material": "Premium Cotton / Silk Blend", "Fit": "Regular Tailored"}
                products_to_create.append(Product(
                    name=pname,
                    slug=slug,
                    category=cat,
                    brand=brand,
                    price=Decimal(str(price)),
                    discount_percent=Decimal(str(random.choice([0, 10, 15, 20, 30]))),
                    stock=random.randint(20, 150),
                    specs=specs,
                    rating=Decimal(str(round(random.uniform(3.7, 4.8), 2))),
                    description=f"{pname} crafted from luxurious, durable fabrics for versatile, contemporary styling."
                ))

    print(f"Generated {len(products_to_create)} total products (including Fashion)...")

    # -------------------------------------------------------------
    # 4. HOME, KITCHEN & APPLIANCES (Target ~100 products)
    # -------------------------------------------------------------
    for name, brand, price, specs in HOME_TEMPLATES:
        for v_num in [1, 2, 3]:
            if len(products_to_create) >= 850:
                break
            variant_name = f"{name} Gen {v_num}" if v_num > 1 else name
            slug = generate_unique_slug(f"{brand} {variant_name}", existing_slugs)
            cat = category_map.get("Kitchen Appliances") if "Air Fryer" in name or "Coffee" in name else (
                category_map.get("Cookware & Dining") if "Pan" in name or "Oven" in name else (
                    category_map.get("Furniture") if "Desk" in name or "Mattress" in name else category_map.get("Smart Home")
                )
            )
            products_to_create.append(Product(
                name=f"{brand} {variant_name}",
                slug=slug,
                category=cat,
                brand=brand,
                price=Decimal(str(price + (v_num - 1) * 500)),
                discount_percent=Decimal(str(random.choice([0, 5, 10, 15]))),
                stock=random.randint(10, 90),
                specs=specs,
                rating=Decimal(str(round(random.uniform(4.0, 4.9), 2))),
                description=f"{brand} {variant_name}. Premium home solution designed to elevate daily comfort, culinary quality, and living spaces."
            ))

    # -------------------------------------------------------------
    # 5. FITNESS & HEALTH (Target ~70 products)
    # -------------------------------------------------------------
    for name, brand, price, specs in FITNESS_TEMPLATES:
        for v_num in [1, 2, 3]:
            if len(products_to_create) >= 920:
                break
            pname = f"{brand} {name}" + (f" Series {v_num}" if v_num > 1 else "")
            slug = generate_unique_slug(pname, existing_slugs)
            cat = category_map.get("Nutrition & Supplements") if "Protein" in name else (
                category_map.get("Gym Equipment") if "Dumbbells" in name else category_map.get("Yoga & Pilates")
            )
            products_to_create.append(Product(
                name=pname,
                slug=slug,
                category=cat,
                brand=brand,
                price=Decimal(str(price)),
                discount_percent=Decimal(str(random.choice([0, 5, 10]))),
                stock=random.randint(25, 200),
                specs=specs,
                rating=Decimal(str(round(random.uniform(4.1, 4.9), 2))),
                description=f"{pname}. Athlete-grade manufacturing engineered for maximum results, purity, and daily conditioning."
            ))

    # -------------------------------------------------------------
    # 6. BOOKS & MEDIA (Fill remaining up to target)
    # -------------------------------------------------------------
    for name, pub, price, specs in BOOK_TEMPLATES:
        for edition in ["1st Edition", "Updated 2nd Edition", "Hardcover Collector", "Paperback"]:
            if len(products_to_create) >= needed_count:
                break
            bname = f"{name} ({edition})"
            slug = generate_unique_slug(bname, existing_slugs)
            specs_copy = dict(specs)
            specs_copy["Edition"] = edition
            products_to_create.append(Product(
                name=bname,
                slug=slug,
                category=category_map.get("Technology & Coding") if "Design" in name or "Code" in name else category_map.get("Self-Help & Business"),
                brand=pub,
                price=Decimal(str(price + (150 if "Hardcover" in edition else 0))),
                discount_percent=Decimal(str(random.choice([0, 10, 15]))),
                stock=random.randint(30, 200),
                specs=specs_copy,
                rating=Decimal(str(round(random.uniform(4.3, 4.95), 2))),
                description=f"{bname} published by {pub}. Essential reading for ambitious builders, leaders, and curious minds."
            ))

    # Bulk create in SQLite in chunks of 200
    print(f"\nBulk saving {len(products_to_create)} new products to SQLite database...")
    created_products = Product.objects.bulk_create(products_to_create, batch_size=200)
    print(f"[OK] Created {len(created_products)} new products successfully!")

    final_count = Product.objects.count()
    print(f"Total Products in NexaCart catalog now: {final_count}")

    # -------------------------------------------------------------
    # 7. SEED AUTHENTIC REVIEWS ACROSS NEW PRODUCTS
    # -------------------------------------------------------------
    seed_reviews_for_new_items()


def seed_reviews_for_new_items():
    """Seed 2-4 customer reviews for products that have 0 reviews."""
    users = list(User.objects.filter(role=User.Role.CUSTOMER))
    if not users:
        print("No customer users found for reviews.")
        return

    unreviewed = Product.objects.filter(reviews__isnull=True).distinct()
    print(f"Seeding customer reviews across {unreviewed.count()} newly added products...")

    REVIEW_POOL = [
        # Beauty / Makeup reviews
        {"rating": 5, "title": "Stays on all day without drying!", "comment": "The shade is absolutely stunning on Indian skin tones. Doesn't smudge or budge even after meals. Definitely worth every rupee."},
        {"rating": 5, "title": "Holy grail cosmetic find", "comment": "High pigment, silky smooth texture, and looks so natural. Comparable to luxury brands costing double the price."},
        {"rating": 4, "title": "Good formula, lovely packaging", "comment": "Formula is lightweight and non-cakey. Finish is beautiful. Minor transfer on coffee cups, but great value for money."},
        {"rating": 4, "title": "Very flattering shade, decent wear", "comment": "Blends like butter into the skin. Looks radiant. Price feels fair for the quantity and packaging quality."},
        {"rating": 3, "title": "Nice shade, but price is slightly steep", "comment": "Product quality is good, but ₹1,200 feels a bit steep when drugstore competitors offer 90% of the same performance for ₹600. Wait for a discount."},
        {"rating": 2, "title": "A bit drying on lips / skin", "comment": "The color is pretty, but feels tight after 3 hours. Needs heavy lip balm or primer underneath. A bit overpriced for this formula."},
        # Tech / Fashion / General reviews
        {"rating": 5, "title": "Exceptional build quality & performance", "comment": "Super fast, clean ergonomics, and looks gorgeous on my desk. Premium purchase that completely pays for itself."},
        {"rating": 4, "title": "Great bang for the buck", "comment": "Very happy with the overall performance and battery life. Pricing is competitive compared to major rivals."},
        {"rating": 3, "title": "Decent, but a bit pricey without bundled accessories", "comment": "Hardware works as advertised, but they should have included a better case at this price tier. A ₹500 price trim would make it perfect."},
        {"rating": 5, "title": "Exceeded all expectations!", "comment": "Delivery was prompt and product is top tier. Would recommend to anyone looking for reliable, authentic quality."}
    ]

    reviews_to_create = []
    for product in unreviewed:
        # Give 2 to 4 reviews per product
        num_reviews = min(random.randint(2, 4), len(users))
        chosen_users = random.sample(users, k=num_reviews)
        for user in chosen_users:
            tpl = random.choice(REVIEW_POOL)
            reviews_to_create.append(Review(
                product=product,
                user=user,
                rating=tpl["rating"],
                title=tpl["title"],
                comment=tpl["comment"]
            ))

    print(f"Bulk saving {len(reviews_to_create)} customer reviews...")
    Review.objects.bulk_create(reviews_to_create, batch_size=300)
    print(f"[OK] Created {len(reviews_to_create)} reviews!")
    print(f"Total reviews in database now: {Review.objects.count()}")


if __name__ == "__main__":
    populate_catalog()
