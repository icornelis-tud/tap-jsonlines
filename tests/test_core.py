"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class, suites
from singer_sdk.testing.templates import TapTestTemplate

from tap_jsonlinesfile.tap import TapJsonLinesFile

SAMPLE_CONFIG = {
    "entity": "test_entity",
    "search_pattern": "tests/data/*.json",
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
}


# Run standard built-in tap tests from the SDK:
TestTapJsonLinesFile = get_tap_test_class(
    tap_class=TapJsonLinesFile, config=SAMPLE_CONFIG, custom_suites=suites()
)


class CustomTest(TapTestTemplate):  # noqa: D101
    name = "custom_test"

    def test(self) -> None:
        """Test stream discovery."""
        streams = self.tap.discover_streams()
        assert len(streams) > 0, "No streams discovered."
        assert any(
            stream.name == "json_array_file" for stream in streams
        ), "Expected 'json_array_file' stream not found."
