Cybsi python SDK
----------------

Software development kit for working with CYBSI API.

### Examples

#### Register generic observation

```python
from datetime import datetime, timezone

from cybsi_sdk import enums
from cybsi_sdk import APIKeyAuth, CybsiClient, ClientConfig
from cybsi_sdk.client import observable
from cybsi_sdk.client import observations

if __name__ == '__main__':
    domain = observable.EntityForm()
    domain.set_type(enums.EntityTypes.DomainName)
    domain.add_key(enums.EntityKeyTypes.String, "test.com")

    generic = observations.GenericObservationForm()
    generic.set_seen_at(datetime.now(timezone.utc))
    generic.set_share_level(enums.ShareLevels.Green)
    generic.add_attribute_fact(
        entity=domain,
        attribute_name=enums.AttributeNames.IsIoC,
        value=True,
        confidence=0.9
    ).add_attribute_fact(
        entity=domain,
        attribute_name=enums.AttributeNames.IsMalicious,
        value=True,
        confidence=0.9
    )

    api_key = "client-key"
    api_url = "http://cybsi.api.com"

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    cfg = ClientConfig(api_url, auth, ssl_verify=False)
    client = CybsiClient(cfg)

    ref = client.observations.generics.register(generic)
    view = client.observations.generics.view(ref.uuid)

```
