import csv
import io

from apps.players.models import Player
from django.db import transaction


class PlayerService:
    @staticmethod
    def bulk_import_from_csv(academy_id, csv_file):
        """
        Imports players from a CSV file.
        Expected format: first_name, last_name, birth_date, registration_number
        """
        from apps.academies.models import Academy

        academy = Academy.objects.get(id=academy_id)

        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        required_fields = ["first_name", "last_name", "birth_date", "registration_number"]
        missing = [f for f in required_fields if f not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"CSV missing required columns: {', '.join(missing)}")

        players_to_create = []
        for row in reader:
            players_to_create.append(
                Player(
                    academy=academy,
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    birth_date=row["birth_date"],
                    registration_number=row["registration_number"],
                )
            )

        with transaction.atomic():
            Player.objects.bulk_create(players_to_create)

        return len(players_to_create)

    @staticmethod
    def get_roster_analytics(group):
        """
        Returns analytics for a specific group.
        """
        total_players = group.players.count()
        # This can be expanded with more complex logic
        return {
            "total_players": total_players,
            "group_name": group.name,
        }
