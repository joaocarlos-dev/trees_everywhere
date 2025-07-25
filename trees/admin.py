from django.contrib import admin
from .models import Tree, PlantedTree


class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    readonly_fields = ('user', 'age', 'planted_at', 'latitude', 'longitude')
    can_delete = False
    show_change_link = True


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')
    inlines = [PlantedTreeInline]
