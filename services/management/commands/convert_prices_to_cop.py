from django.core.management.base import BaseCommand
from services.models import Service, ServiceFeature
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP

class Command(BaseCommand):
    help = 'Convierte precios almacenados en USD a COP usando la tasa en settings (USD_TO_COP_RATE) y actualiza price_currency a COP'

    def handle(self, *args, **options):
        usd_to_cop = Decimal(getattr(settings, 'USD_TO_COP_RATE', 4700))
        services = Service.objects.all()
        updated = 0
        for s in services:
            if s.price_from and s.price_currency and s.price_currency != 'COP':
                original = Decimal(s.price_from)
                converted = (original * usd_to_cop).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                s.price_from = converted
                s.price_currency = 'COP'
                s.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Converted {s.title}: {original} -> {converted} COP'))

        # Convertir additional_cost en ServiceFeature
        features = ServiceFeature.objects.filter(additional_cost__isnull=False)
        feat_updated = 0
        for f in features:
            if f.additional_cost and f.additional_cost != 0:
                original = Decimal(f.additional_cost)
                # Asumimos que adicional estaba en USD si la moneda general era USD; no hay campo de moneda aquí
                converted = (original * usd_to_cop).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
                f.additional_cost = converted
                f.save()
                feat_updated += 1
                self.stdout.write(self.style.SUCCESS(f'Converted feature {f.title}: {original} -> {converted}'))

        self.stdout.write(self.style.SUCCESS(f'Updated {updated} services and {feat_updated} features to COP'))
