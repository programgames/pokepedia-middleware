from pokeapi.pokemon_v2.models import *


class MoveNameChangelog(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    generation = models.ForeignKey(
        "pokemon_v2.Generation",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        "pokemon_v2.Type",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )
    move = models.ForeignKey(
        "pokemon_v2.Move",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )
    language = models.ForeignKey(
        "pokemon_v2.Language",
        blank=True,
        null=True,
        related_name="%(class)s_language",
        on_delete=models.CASCADE,
    )
    pass

class PkmAvailabilityForm(models.Model):
    parent = models.ForeignKey('PokemonMoveAvailability', related_name='parent_form', on_delete=models.CASCADE)
    child = models.ForeignKey('PokemonMoveAvailability', related_name='child_form', on_delete=models.CASCADE)
    version_group = models.ForeignKey('pokemon_v2.VersionGroup', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('parent', 'child', 'version_group'),)

    def __str__(self):
        return f"Form link between {self.parent} and {self.child} in {self.version_group}"


class HasMachine(models.Model):
    machine = models.ForeignKey(
        "pokemon_v2.Machine",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class PokemonMoveAvailability(HasMachine):
    pokemon = models.ForeignKey(
        "pokemon_v2.Pokemon",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )
    version_group = models.ForeignKey(
        "pokemon_v2.VersionGroup",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )
    is_default = models.BooleanField(default=True)
    has_pokepedia_page = models.BooleanField(default=True)
    level = models.BooleanField(default=True)
    tutor = models.BooleanField(default=True)
    egg = models.BooleanField(default=True)
    forms = models.ForeignKey(
        "PkmAvailabilityForm",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.pokemon} in {self.version_group}"

class CacheItem(models.Model):
    key = models.TextField(null=False)
    data = models.JSONField(null=False)
