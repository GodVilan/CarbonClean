import json
from django.core.management.base import BaseCommand
from CarbonEmission.models import StepCategory, StepSubCategory, Step
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Load steps data into the database"

    def handle(self, *args, **kwargs):
        steps_file_path = os.path.join(settings.BASE_DIR, 'CarbonEmission', 'static', 'json', 'steps_to_minimize.json')
        
        with open(steps_file_path, 'r', encoding = 'utf-8') as steps_file:
            data = json.load(steps_file)

        for category, subcategories in data.items():
            if category == "GeneralRecommendations":
                continue

            category_obj, _ = StepCategory.objects.get_or_create(name=category)

            for subcategory, cases in subcategories.items():
                subcategory_obj, _ = StepSubCategory.objects.get_or_create(
                    category=category_obj, name=subcategory
                )

                for case, steps in cases.items():
                    for step in steps:
                        Step.objects.get_or_create(
                            sub_category=subcategory_obj,
                            case=case,
                            description=step,
                        )

        self.stdout.write(self.style.SUCCESS("Steps data loaded successfully!"))
