import uuid
from datetime import datetime
from typing import Optional, List, cast

from cybsi.utils.converters import convert_relationship_kind_kebab

from .entity import EntityView, ValuableFactView
from .enums import RelationshipKinds
from ..internal import (
    BaseAPI,
    JsonObjectView,
    rfc3339_timestamp,
)


class RelationshipsAPI(BaseAPI):
    """Entities API."""

    _path = "/observable/relationships"

    def forecast(
        self,
        source_entity_uuid: uuid.UUID,
        target_entity_uuid: uuid.UUID,
        kind: RelationshipKinds,
        forecast_at: Optional[datetime] = None,
        valuable_facts: Optional[bool] = None,
    ) -> "RelationshipsForecastView":
        """Get forecast of relationship between two entities.

        Note:
            Calls `GET /observable/relationships
                /{sourceEntityUUID}/{relationKind}/{targetEntityUUID}`.
        Args:
            source_entity_uuid: Source entity UUID.
            kind: Kind of relationship. Converts to kebab-case on URL-path.
            target_entity_uuid: Target entity UUID.
            forecast_at: Date of forecast.
                If not specified, forecast is built on current time.
            valuable_facts: Attach list of valuable facts to forecast.
        Returns:
            Relationship forecast view.
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import RelationshipType
            >>> client: CybsiClient
            >>> forecasts = client.observable.relationships.forecast(
            >>>     UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     RelationshipKind.ResolvesTo,
            >>> )
            >>> # Do something with the forecast
            >>> print(forecast)
        """
        kebab_kind = convert_relationship_kind_kebab(kind)
        path = f"{self._path}/{source_entity_uuid}/{kebab_kind}/{target_entity_uuid}"
        params = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if valuable_facts is not None:
            params["valuableFacts"] = valuable_facts  # type: ignore
        r = self._connector.do_get(path=path, params=params)
        return RelationshipsForecastView(r.json())


class RelationshipsForecastView(JsonObjectView):
    """Relationship forecast view."""

    @property
    def relationship(self) -> "RelationshipView":
        """Relationship view."""
        return RelationshipView(self._get("relationship"))

    @property
    def confidence(self) -> float:
        """Relationship forecast confidence.
        0 if there's no valuable facts about the relationship."""
        return self._get("confidence")

    @property
    def valuable_facts(self) -> Optional[List["ValuableFactView"]]:
        """List of forecast valuable facts in descending order of confidence."""
        return self._map_list_optional("valuableFacts", ValuableFactView)


class RelationshipView(JsonObjectView):
    """Relationship fact view."""

    @property
    def source(self) -> EntityView:
        """Relationship's source entity.

        Warning:
            Ref uuid may be zero uuid,
            if source entity keys were invalid during registration.
        """

        return EntityView(self._get("source"))

    @property
    def kind(self) -> RelationshipKinds:
        """Kind of the relationship."""

        return RelationshipKinds(self._get("kind"))

    @property
    def target(self) -> EntityView:
        """Target entity.

        Warning:
            Ref uuid may be zero uuid,
            if source entity keys were invalid during registration.
        """

        return EntityView(self._get("target"))

    @property
    def confidence(self) -> float:
        """Relationship fact confidence."""

        return float(cast(float, self._get("confidence")))