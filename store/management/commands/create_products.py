from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates sample categories and products'

    def handle(self, *args, **kwargs):
        # Create Categories
        electronics, _ = Category.objects.get_or_create(
            name="Electronics",
            slug="electronics",
            description="Electronic items and gadgets"
        )
        
        clothing, _ = Category.objects.get_or_create(
            name="Clothing",
            slug="clothing",
            description="Fashion and apparel"
        )
        
        books, _ = Category.objects.get_or_create(
            name="Books",
            slug="books",
            description="Books and literature"
        )

        # Create Electronics Products
        Product.objects.get_or_create(
            name="Wireless Headphones",
            category=electronics,
            price=Decimal("99.99"),
            digital=True,
            description="High-quality wireless headphones with noise cancellation",
            stock=10
        )

        Product.objects.get_or_create(
            name="Smart Watch",
            category=electronics,
            price=Decimal("199.99"),
            digital=False,
            description="Smart watch with fitness tracking and notifications",
            stock=15
        )

        Product.objects.get_or_create(
            name="Gaming Laptop",
            category=electronics,
            price=Decimal("1299.99"),
            digital=True,
            description="High-performance gaming laptop with RTX 3080",
            stock=5
        )

        # Create Clothing Products
        Product.objects.get_or_create(
            name="Denim Jeans",
            category=clothing,
            price=Decimal("49.99"),
            digital=False,
            description="Classic blue denim jeans",
            stock=20
        )

        Product.objects.get_or_create(
            name="Cotton T-Shirt",
            category=clothing,
            price=Decimal("24.99"),
            digital=False,
            description="Comfortable cotton crew neck t-shirt",
            stock=30
        )

        Product.objects.get_or_create(
            name="Running Shoes",
            category=clothing,
            price=Decimal("79.99"),
            digital=False,
            description="Professional running shoes with cushioning",
            stock=12
        )

        # Create Books Products
        Product.objects.get_or_create(
            name="Python Programming Guide",
            category=books,
            price=Decimal("39.99"),
            digital=True,
            description="Comprehensive guide to Python programming",
            stock=25
        )

        Product.objects.get_or_create(
            name="Best Novels Collection",
            category=books,
            price=Decimal("89.99"),
            digital=False,
            description="Collection of bestselling novels",
            stock=8
        )

        Product.objects.get_or_create(
            name="World Cuisine Cookbook",
            category=books,
            price=Decimal("29.99"),
            digital=False,
            description="Recipes from around the world",
            stock=15
        )

        self.stdout.write(self.style.SUCCESS('Successfully created categories and products')) 