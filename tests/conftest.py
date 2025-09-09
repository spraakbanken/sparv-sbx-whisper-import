import os

import pytest
import sparv
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture(name="sparv_datadir", scope="session")
def fixture_sparv_datadir() -> str:
    home_env = os.environ.get("HOME")
    print(f"$HOME={home_env}")  # noqa: T201
    if os.environ.get("GITHUB_ACTIONS", "false") == "true":
        return f"{home_env}/.local/share/sparv"
    return f"{home_env}/.config/sparv"


@pytest.fixture(scope="session")
def setup_sparv(sparv_datadir: str) -> None:
    with sparv.call(["setup", "--dir", sparv_datadir]) as sparv_call:
        for log_messages in sparv_call:
            print(log_messages)  # noqa: T201
        assert sparv_call.get_return_value()


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)
