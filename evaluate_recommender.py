"""
Offline AI Evaluation Script for NexaCart Recommender
Calculates Precision@K and NDCG@K to evaluate recommendation quality
against historical user interactions.
"""
import os
import sys
import django
import math


# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps'))
django.setup()

from accounts.models import User
from recommendations.models import Interaction, UserPreference
from products.models import Product

def get_relevant_products(user):
    """
    Define 'ground truth' relevant products for a user.
    We consider a product relevant if the user has purchased, carted, or wishlisted it.
    """
    strong_interactions = [
        Interaction.InteractionType.PURCHASE,
        Interaction.InteractionType.CART,
        Interaction.InteractionType.WISHLIST
    ]
    interactions = Interaction.objects.filter(
        user=user, 
        interaction_type__in=strong_interactions
    ).values_list('product_id', flat=True).distinct()
    
    return set(interactions)


def get_recommendations(user, k=10):
    """
    Get top K recommendations using the v1 engine logic.
    """
    top_cats = UserPreference.objects.filter(user=user, category__isnull=False).order_by('-score')[:3]
    cat_ids = [p.category_id for p in top_cats]
    
    recommended = list(Product.objects.filter(
        category_id__in=cat_ids,
        stock__gt=0
    ).order_by('-rating').values_list('id', flat=True)[:k])
    
    # Cold start fallback
    if not recommended:
        recommended = list(Product.objects.filter(stock__gt=0).order_by('-rating').values_list('id', flat=True)[:k])
        
    return recommended


def calculate_precision_at_k(recommended_ids, relevant_ids, k):
    """Calculate Precision@K: (Relevant items in top K) / K"""
    if not recommended_ids or k == 0:
        return 0.0
    
    recommended_k = recommended_ids[:k]
    hits = sum(1 for item in recommended_k if item in relevant_ids)
    return hits / k


def calculate_ndcg_at_k(recommended_ids, relevant_ids, k):
    """Calculate NDCG@K: DCG@K / IDCG@K"""
    if not recommended_ids or not relevant_ids or k == 0:
        return 0.0
        
    recommended_k = recommended_ids[:k]
    
    # Calculate DCG
    dcg = 0.0
    for i, item_id in enumerate(recommended_k):
        if item_id in relevant_ids:
            # relevance score is 1 (binary relevance)
            dcg += 1.0 / math.log2(i + 2) # i+2 because index is 0-based and log2(1) = 0
            
    # Calculate IDCG (Ideal DCG)
    idcg = 0.0
    ideal_hits = min(len(relevant_ids), k)
    for i in range(ideal_hits):
        idcg += 1.0 / math.log2(i + 2)
        
    if idcg == 0:
        return 0.0
        
    return dcg / idcg


def run_evaluation():
    print("=" * 50)
    print("Evaluating NexaCart Recommender Engine")
    print("=" * 50)
    
    users = User.objects.filter(role=User.Role.CUSTOMER)
    
    p5_scores = []
    p10_scores = []
    ndcg10_scores = []
    
    evaluated_users = 0
    
    for user in users:
        relevant_ids = get_relevant_products(user)
        # Only evaluate users who actually have relevant history to test against
        if not relevant_ids:
            continue
            
        recommended_ids = get_recommendations(user, k=10)
        
        p5 = calculate_precision_at_k(recommended_ids, relevant_ids, k=5)
        p10 = calculate_precision_at_k(recommended_ids, relevant_ids, k=10)
        ndcg10 = calculate_ndcg_at_k(recommended_ids, relevant_ids, k=10)
        
        p5_scores.append(p5)
        p10_scores.append(p10)
        ndcg10_scores.append(ndcg10)
        
        evaluated_users += 1
        
    if evaluated_users == 0:
        print("No users with sufficient interaction history found. Run seed_data.py first.")
        return
        
    mean_p5 = sum(p5_scores) / len(p5_scores)
    mean_p10 = sum(p10_scores) / len(p10_scores)
    mean_ndcg10 = sum(ndcg10_scores) / len(ndcg10_scores)
    
    print(f"Evaluated {evaluated_users} users with interaction history.")
    print("-" * 50)
    print(f"Metrics (Binary Relevance based on past purchases/carts):")
    print(f"Mean Precision@5:  {mean_p5:.4f}  ({mean_p5*100:.1f}%)")
    print(f"Mean Precision@10: {mean_p10:.4f}  ({mean_p10*100:.1f}%)")
    print(f"Mean NDCG@10:      {mean_ndcg10:.4f}  ({mean_ndcg10*100:.1f}%)")
    print("=" * 50)


if __name__ == "__main__":
    run_evaluation()

