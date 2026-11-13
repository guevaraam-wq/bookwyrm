"""Characterization tests for the RedisStore base class."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from bookwyrm.redis_store import RedisStore


class ExampleStore(RedisStore):
    """Concrete implementation used to test RedisStore behavior."""

    def get_rank(self, obj):
        return obj.rank

    def get_objects_for_store(self, store):
        return []


@pytest.fixture
def store():
    instance = ExampleStore()
    instance.max_length = 10
    return instance


def test_add_object_when_stores_exist_adds_and_trims_each_store(store):
    """Adding an object queues a ranked insert and trim for each store."""
    obj = SimpleNamespace(id=42, rank=100)
    pipeline = MagicMock()

    with patch("bookwyrm.redis_store.r.pipeline", return_value=pipeline):
        store.add_object_to_stores(obj, ["feed-a", "feed-b"])

    pipeline.zadd.assert_any_call("feed-a", {42: 100})
    pipeline.zadd.assert_any_call("feed-b", {42: 100})
    pipeline.zremrangebyrank.assert_any_call("feed-a", 0, -10)
    pipeline.zremrangebyrank.assert_any_call("feed-b", 0, -10)
    assert pipeline.zadd.call_count == 2
    assert pipeline.zremrangebyrank.call_count == 2
    pipeline.execute.assert_called_once_with()


def test_add_object_when_stores_empty_executes_empty_pipeline(store):
    """An empty list queues no writes but still executes the pipeline."""
    obj = SimpleNamespace(id=42, rank=100)
    pipeline = MagicMock()

    with patch("bookwyrm.redis_store.r.pipeline", return_value=pipeline):
        store.add_object_to_stores(obj, [])

    pipeline.zadd.assert_not_called()
    pipeline.zremrangebyrank.assert_not_called()
    pipeline.execute.assert_called_once_with()


def test_add_object_when_redis_fails_propagates_error(store):
    """A Redis execution failure is propagated to the caller."""
    obj = SimpleNamespace(id=42, rank=100)
    pipeline = MagicMock()
    pipeline.execute.side_effect = RedisConnectionError("Redis unavailable")

    with patch("bookwyrm.redis_store.r.pipeline", return_value=pipeline):
        with pytest.raises(RedisConnectionError, match="Redis unavailable"):
            store.add_object_to_stores(obj, ["feed-a"])

    pipeline.zadd.assert_called_once_with("feed-a", {42: 100})
    pipeline.execute.assert_called_once_with()


def test_add_object_deferred_returns_pipeline_without_executing(store):
    """Callers can queue writes and execute the returned pipeline later."""
    obj = SimpleNamespace(id=42, rank=100)
    pipeline = MagicMock()
    with patch("bookwyrm.redis_store.r.pipeline", return_value=pipeline):
        result = store.add_object_to_stores(obj, ["feed-a"], execute=False)
    assert result is pipeline
    pipeline.zadd.assert_called_once_with("feed-a", {42: 100})
    pipeline.execute.assert_not_called()
