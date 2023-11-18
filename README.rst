colcon-top-level-workspace
==========================

An extension for `colcon-core <https://github.com/colcon/colcon-core>`_ to allow running from any subfolder of a workspace.

This package allows to run colcon from any subfolder of a colcon workspace, but reusing
existing `build`, `install`, and `log` folders from the top-level workspace.
The root of the workspace is determined by looking for the .colcon_root marker file.
Alternatively, the existince of `build`, `install`, and `log` folders indicates the root folder.
