# Workspace layout

The project root at `/workspaces/lightning/` is a plain directory containing
two sibling Git repositories:

- `/workspaces/lightning/lightning/` is the PyTorch Lightning repository. Run
  source Git commands, inspect diffs, and make source changes there.
- `/workspaces/lightning/workspace/` owns the devcontainer configuration,
  notes, and local experiments. Experiments live directly in this repository
  and do not belong to the PyTorch Lightning repository unless a task
  explicitly moves the work there.

The `.devcontainer` entry at the project root is a symlink into the workspace
repository. Keep the two repositories as siblings; do not turn the source
checkout into a submodule or nest it inside the workspace repository.
