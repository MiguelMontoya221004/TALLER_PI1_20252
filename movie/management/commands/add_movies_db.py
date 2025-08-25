# movie/management/commands/add_movies_db.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from movie.models import Movie
from pathlib import Path
import json

class Command(BaseCommand):
    help = "Carga (o actualiza) hasta 100 películas desde movies.json al modelo Movie."

    def handle(self, *args, **kwargs):
        # Ajusta esta ruta según dónde tengas el archivo
        # Opción A: si movies.json está en movie/movies.json
        json_path = Path(settings.BASE_DIR) / "movie" / "management" / "commands" / "movies.json"


        # Opción B (descomenta si lo tienes en management/commands/)
        # json_path = Path(settings.BASE_DIR) / "movie" / "management" / "commands" / "movies.json"

        if not json_path.exists():
            raise CommandError(f"No se encontró el archivo JSON en: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            movies = json.load(f)

        created, updated = 0, 0

        for m in movies[:100]:   # limita a 100
            # Mapea las claves del JSON a tu modelo. Ajusta si tus nombres difieren.
            title = m.get("title")
            genre = m.get("genre") or ""
            year = m.get("year")
            description = m.get("plot") or ""

            # Convierte year a int si tu campo es IntegerField
            try:
                year = int(year) if year not in (None, "", "N/A") else None
            except ValueError:
                year = None

            # Usa update_or_create para evitar duplicados por título
            obj, was_created = Movie.objects.update_or_create(
                title=title,
                defaults={
                    "image": "movie/images/default.png",  # Ajusta a tu ImageField / MEDIA_ROOT
                    "genre": genre,
                    "year": year,
                    "description": description,
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Listo ✅  Creadas: {created} | Actualizadas: {updated} | Total procesadas: {min(100, len(movies))}"
        ))
