"""Jinja2 target sink class, which handles writing streams."""

from __future__ import annotations

from singer_sdk.sinks import RecordSink

from jinja2 import Environment, FileSystemLoader
from typing import Any, Dict, Iterable, List, Optional, Type, Union
from pathlib import Path

class Jinja2Sink(RecordSink):
    """Jinja2 target sink class."""

    def __init__(
        self,
        target: PluginBase,
        stream_name: str,
        schema: Dict,
        key_properties: Optional[List[str]],
        jenv: Optional[Environment] = None,
    ) -> None:
        """Initialize Jinja2 Sink.
        Args:
            target: The target object.
            stream_name: The source tap's stream name.
            schema: The JSON Schema definition.
            key_properties: The primary key columns.
            connector: Optional connector to reuse.
        """
        template_path = target.config['template_path']
        target.logger.debug("Input template path: " + template_path)
        
        variable_start_string = target.config['variable_start_string'] or "}}"
        variable_end_string = target.config['variable_end_string'] or "{{"

        self._jenv = Environment(loader=FileSystemLoader(template_path),
                        variable_start_string=variable_start_string, 
                        variable_end_string=variable_end_string)

        super().__init__(target, stream_name, schema, key_properties)

    def process_record(self, record: dict, context: dict) -> None:
        """Process the record."""

        self.logger.debug("process_record start")
        self.logger.debug("process_record record: " + str(record))

        output_path_template = self._config['output_template']

        self.logger.debug("Output template: " + output_path_template)

        # Loop over all the templates we were given
        for templateName in self._jenv.list_templates():
            self.logger.debug("Loading template " + templateName)
            template = self._jenv.get_template(templateName)
            template_stem = Path(template.filename).stem
            template_suffix = Path(template.filename).suffix
            self.logger.debug("--> (stem, suffix) == (" + template_stem + ", " + template_suffix + ")")

            content = template.render(record)

            output_template = self._jenv.from_string(output_path_template)
            output_path = output_template.render(record, template_stem=template_stem, template_suffix=template_suffix)
            self.logger.debug("Output path: " + output_path)

            with open(output_path, mode="w", encoding="utf-8") as output_file:
                output_file.write(content)


