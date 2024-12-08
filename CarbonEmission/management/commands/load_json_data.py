import json
import os
from django.core.management.base import BaseCommand
from CarbonEmission.models import SubCategoryEffect, SubCategorySolution
from django.conf import settings

class Command(BaseCommand):
    help = 'Load subcategory effects and solutions into the database'

    def handle(self, *args, **kwargs):
        effects_file_path = os.path.join(settings.BASE_DIR, 'CarbonEmission', 'static', 'json', 'sub_cat_effect.json')
        solutions_file_path = os.path.join(settings.BASE_DIR, 'CarbonEmission', 'static', 'json', 'sub_cat_sol.json')

        with open(effects_file_path, 'r', encoding = 'utf-8') as effects_file:
            effects_data = json.load(effects_file)

        for category, subcategories in effects_data.items():
            for sub_category, effects in subcategories.items():
                for title, description in effects.items():
                    SubCategoryEffect.objects.get_or_create(
                        category=category,
                        sub_category=sub_category,
                        effect_title=title,
                        effect_description=description
                    )

        with open(solutions_file_path, 'r', encoding = 'utf-8') as solutions_file:
            solutions_data = json.load(solutions_file)

        for category, subcategories in solutions_data.items():
            for sub_category, solutions in subcategories.items():
                for title, description in solutions.items():
                    SubCategorySolution.objects.get_or_create(
                        category=category,
                        sub_category=sub_category,
                        solution_title=title,
                        solution_description=description
                    )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
