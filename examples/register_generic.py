#!/usr/bin/env python3
from os import environ
from datetime import datetime, timezone

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.observable import (
    AttributeNames,
    EntityForm,
    EntityKeyTypes,
    EntityTypes,
    ShareLevels,
    RelationshipKinds,
)
from cybsi.api.observation import GenericObservationForm


def create_generic_observation():
    domain = EntityForm(EntityTypes.DomainName)
    domain.add_key(EntityKeyTypes.String, "test.com")

    ip_address = EntityForm(EntityTypes.IPAddress)
    ip_address.add_key(EntityKeyTypes.String, "8.8.8.8")

    observation = (
        GenericObservationForm(
            share_level=ShareLevels.Green, seen_at=datetime.now(timezone.utc)
        )
        .add_attribute_fact(
            entity=domain,
            attribute_name=AttributeNames.IsIoC,
            value=True,
            confidence=0.9,
        )
        .add_attribute_fact(
            entity=domain,
            attribute_name=AttributeNames.IsMalicious,
            value=True,
            confidence=0.9,
        )
        .add_entity_relationship(
            source=domain,
            kind=RelationshipKinds.Resolves,
            target=ip_address,
            confidence=0.5,
        )
    )
    return observation


if __name__ == "__main__":
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    generic_observation = create_generic_observation()
    ref = client.observations.generics.register(generic_observation)
    view = client.observations.generics.view(ref.uuid)