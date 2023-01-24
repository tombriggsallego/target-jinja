"""Jinja2 target class."""

from __future__ import annotations

from singer_sdk.target_base import Target
from singer_sdk import typing as th

from target_jinja.sinks import (
    Jinja2Sink,
)


class TargetJinja2(Target):
    """Sample target for Jinja2."""

    name = "target-jinja"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "template_path",
            th.StringType,
            description="The path to the target template directory"
        ),
        th.Property(
            "output_template",
            th.StringType,
            description="The Jinja template string with which output files will be named"
        ),
        th.Property(
            "variable_start_string",
            th.StringType,
            description="The string marking the beginning of a print statement"
        ),
        th.Property(
            "variable_end_string",
            th.StringType,
            description="The string marking the end of a print statement"
        ),
    ).to_dict()

    default_sink_class = Jinja2Sink


if __name__ == "__main__":
    TargetJinja2.cli()
