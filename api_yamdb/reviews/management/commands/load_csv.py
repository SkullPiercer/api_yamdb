import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.shortcuts import get_object_or_404

from api_yamdb import settings


folder_path = settings.BASE_DIR / "static" / "data"
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

FOREIGNKEY_FIELDS = ("category", "author", "genre", "title", "review")

class Command(BaseCommand):
    help = 'Загрузка данных моделей в БД SQLite3 из файлов .CSV '
    FILE_NAMES = []
    for csv_file_name in csv_files:
        FILE_NAMES.append(csv_file_name)

    def get_model(self, model_name):
        """Возвращает имя модели по полю из csv файла."""
        if model_name == "author":
            Model = apps.get_model("reviews", "user")
        elif model_name == "comments":
            Model = apps.get_model("reviews", "comment")
        else:
            Model = apps.get_model("reviews", model_name)
        if not Model:
            raise CommandError(f"Модели {Model} не существует")
        return Model

    def handle(self, *args, **options):
        for name in self.FILE_NAMES:
            new_name = os.path.splitext(name)[0]
            model = self.get_model(new_name)
            path = settings.BASE_DIR / "static" / "data" / name

            with open(f'{path}', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Obj = model(**row)
                    for i, field in enumerate(row.values()):
                        if reader.fieldnames[i] in FOREIGNKEY_FIELDS:
                            model = self.get_model(reader.fieldnames[i])
                            obj = get_object_or_404(model, id=field)
                            setattr(Obj, reader.fieldnames[i], obj)
                        else:
                            setattr(Obj, reader.fieldnames[i], field)
                    Obj.save()
