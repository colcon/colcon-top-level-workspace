# Copyright 2023 Scott K Logan
# Licensed under the Apache License, Version 2.0

import os
from pathlib import Path

from colcon_core.argument_parser import ArgumentParserDecoratorExtensionPoint
from colcon_core.argument_parser import SuppressUsageOutput
from colcon_core.argument_parser.action_collector \
    import ActionCollectorDecorator
from colcon_core.argument_parser.action_collector \
    import SuppressRequiredActions
from colcon_core.argument_parser.action_collector \
    import SuppressTypeConversions
from colcon_core.plugin_system import satisfies_version


class TopLevelWorkspaceArgumentParserDecorator(
    ArgumentParserDecoratorExtensionPoint
):
    """Locate and use a top-level workspace from a subdirectory."""

    # Lower priority to appear as close to time-of-use as possible
    PRIORITY = 75

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            ArgumentParserDecoratorExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.0')

    def decorate_argument_parser(self, *, parser):  # noqa: D102
        return TopLevelWorkspaceArgumentDecorator(parser)


def _enumerate_parsers(parser):
    yield from parser._parsers
    for subparser in parser._subparsers:
        for p in subparser._parsers:
            yield p
            yield from _enumerate_parsers(p)


class TopLevelWorkspaceArgumentDecorator(ActionCollectorDecorator):
    """Change to a top-level workspace if one is found."""

    def __init__(self, parser):  # noqa: D107
        # avoid setting members directly, the base class overrides __setattr__
        # pass them as keyword arguments instead
        super().__init__(
            parser,
            _parsers=[],
            _subparsers=[])

    def add_parser(self, *args, **kwargs):
        """Collect association of parsers to their name."""
        parser = super().add_parser(*args, **kwargs)
        self._parsers.append(parser)
        return parser

    def add_subparsers(self, *args, **kwargs):
        """Collect all subparsers."""
        subparser = super().add_subparsers(*args, **kwargs)
        self._subparsers.append(subparser)
        return subparser

    def parse_args(self, *args, **kwargs):  # noqa: D102
        parsers = [self._parser]
        parsers.extend(_enumerate_parsers(self))
        with SuppressUsageOutput(parsers):
            with SuppressTypeConversions(parsers):
                with SuppressRequiredActions(parsers):
                    known_args, _ = self._parser.parse_known_args(
                        *args, **kwargs)

        base = 'build'
        for arg in ('build_base', 'test_result_base'):
            if hasattr(known_args, arg):
                base = getattr(known_args, arg)
                break
        if not os.path.isabs(base):
            cwd = Path.cwd()
            workspace = find_top_level_workspace(cwd, base)
            if workspace and workspace != cwd:
                print(f"Using top-level workspace at '{workspace}'")
                os.chdir(str(workspace))
        args = self._parser.parse_args(*args, **kwargs)
        return args


def find_top_level_workspace(candidate, base, this_build_tool='colcon'):
    """
    Search for an existing top-level colcon workspace.

    :param candidate: Directory at which the search should begin
    :param str base: The base directory
    :param str this_build_tool: The name of this build tool

    :returns: Path to an existing workspace root, or None
    """
    marker = candidate / base / '.built_by'
    if marker.is_file():
        if marker.read_text().rstrip() == this_build_tool:
            return candidate
    if candidate.parent != candidate:
        return find_top_level_workspace(
            candidate.parent, base, this_build_tool)
    return None
