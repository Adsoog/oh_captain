from core.models import Period
from django.core.management.base import BaseCommand
from django.utils.timezone import datetime, timedelta


class Command(BaseCommand):
    help = "Crea los períodos mensuales para un año específico"

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Año para el que se crearán los períodos')

    def handle(self, *args, **options):
        year = options['year']
        months = [
            ('ENE', 1), ('FEB', 2), ('MAR', 3), ('ABR', 4), ('MAY', 5), ('JUN', 6),
            ('JUL', 7), ('AGO', 8), ('SEP', 9), ('OCT', 10), ('NOV', 11), ('DIC', 12)
        ]

        for month_abbr, month_num in months:
            start_date = datetime(year, month_num, 1).date()
            if month_num == 12:
                end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
            else:
                end_date = datetime(year, month_num + 1, 1).date() - timedelta(days=1)

            period_name = f"{month_abbr}{year}"
            period, created = Period.objects.get_or_create(
                name=period_name,
                defaults={'start_date': start_date, 'end_date': end_date, 'is_active': True}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Período creado: {period_name} ({start_date} - {end_date})"))
            else:
                self.stdout.write(self.style.WARNING(f"El período {period_name} ya existe."))

