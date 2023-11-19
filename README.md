colcon-top-level-workspace
==========================

An extension for [`colcon-core`](https://github.com/colcon/colcon-core) to allow running from any subfolder of a workspace.

This package allows running `colcon` from any subfolder of a colcon workspace, but reusing
existing `build`, `install`, and `log` folders from the root folder of the workspace.

The root of the workspace is determined by looking for the `.colcon_root` marker file, which is created on first invocation.
Alternatively, the existence of `build`, `install`, and `log` folders indicates the root folder.

Package discovery is done relative to the current working directory. Thus, to build all packages in the current folder, just run `colcon build`.
To build all packages in the workspace, specify the special token `ROOT` for the `--base-paths` argument: `colcon build --base-paths ROOT`.