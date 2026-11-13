"""Regression tests for the number of ranked entries retained in a store."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import fakeredis
import pytest

from bookwyrm.redis_store import RedisStore


class CapacityStore(RedisStore):
    """Rank objects by a supplied score without database or network access."""

    def get_rank(self, obj):
        return obj.rank

    def get_objects_for_store(self, store):
        return self.objects


@pytest.mark.parametrize("method", ["single", "bulk", "populate"])
@pytest.mark.parametrize("capacity", [1, 10])
@pytest.mark.parametrize("offset", [-1, 0, 1], ids=["below", "at", "above"])
def test_store_retains_capacity_highest_ranked_entries(method, capacity, offset):
    """Retain all entries up to capacity and discard only the lowest overflow."""
    store = CapacityStore()
    store.max_length = capacity
    count = capacity + offset
    # Bulk/population querysets supply the highest-ranked objects first.
    objects = [SimpleNamespace(id=i, rank=i) for i in range(count, 0, -1)]
    queryset = MagicMock()
    queryset.__getitem__.side_effect = objects.__getitem__
    queryset.exists.return_value = bool(objects)
    store.objects = queryset

    with patch("bookwyrm.redis_store.r", fakeredis.FakeRedis()):
        if method == "single":
            for obj in objects:
                store.add_object_to_stores(obj, ["feed"])
        elif method == "bulk":
            store.bulk_add_objects_to_store(queryset, "feed")
        else:
            store.populate_store("feed")

        retained = store.get_store("feed")

    expected = [str(obj.id).encode("ascii") for obj in objects[:capacity]]
    assert retained == expected
    assert len(retained) == min(count, capacity)
