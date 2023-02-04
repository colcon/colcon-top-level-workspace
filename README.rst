colcon-top-level-workspace
==========================

An extension for `colcon-core <https://github.com/colcon/colcon-core>`_ to locate and use a top-level workspace when in subdirectories thereof.

This package looks for marker files created by colcon which infer the root of a workspace.
Depending on the your workspace configuration, additional heuristics may be necessary to handle corner cases.
