from django.utils import timezone
from haystack import indexes

from .models import BaseProduct


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    product = indexes.CharField(model_attr='name')

    def get_model(self):
        return BaseProduct

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created_at__lte=timezone.now())
