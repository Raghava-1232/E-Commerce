from django.core.management.base import BaseCommand
from store.models import Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads product images from fixtures'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            if product.image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if not os.path.exists(image_path):
                    self.stdout.write(
                        self.style.WARNING(f'Image not found for {product.name}: {image_path}')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'Image found for {product.name}')
                    ) 