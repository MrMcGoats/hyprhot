# About
This is a script for hyprland.
This python script, along with the socket listener, helps on workspace management when hotplugging 
monitors.

Typical use case: When using a laptop, there may be multiple physical locations, e.g. home and office,
with different external monitors.
If one wants to have the same workspaces with the same keyboard shortcuts for switching assigned
to different monitors on different locations, this is currently problematic with hyprland,
as only one workspace rule applies at the same time for a workspace.
Hence, it is not possible to use something like
```
workspace = name:external_1,monitor:desc:Dell Inc. DELL P2314H J8J313CPAFML,default:true
workspace = name:external_1,monitor:desc:Lenovo Group Limited T24i-30 VTQ05862,default:true
```
The intended behavior is that workspace `external_1` is always assigned to that one of the two monitors
that is actually connected.
Currently, this doesn't seem to work as the last workspace rule takes precedence.

Also, there is the annoying case that one uses a notebook without external monitors first,
and switches to workspace, e.g, `external_1` on the notebook's monitor.
Then, when hotplugging the external monitor, the workspace will still be assigned to the notebook's monitor.

This script tries to make workspace handling in this situations a bit easier:
Possible monitor - workspace configurations are given in the config.
On hotplug, workspace rules for the connected monitors are created dynamically based on the config.
Also, existing workspaces are re-assigned to the monitors they are intendet to be assigned to.

# Usage
1. Create a config. An example config is provided in the repository:
    ```
   [
    {
    "description": "AU Optronics 0x623D",
    "workspaces": [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9"
    ],
    "workspace_default": "1"
    },
    {
      "description": "Dell Inc. DELL UP2516D 3JV405AG097L",
      "workspaces": [
        "external_1",
        "external_2",
        "external_3",
        "external_4",
        "external_5",
        "external_6",
        "external_7",
        "external_8",
        "external_9"
      ],
      "workspace_default": "external_1"
    },
      {
      "description": "Lenovo Group Limited T24i-30 VTQ05862",
      "workspaces": [
              "external_1",
              "external_2",
              "external_3",
              "external_4"
      ],
      "workspace_default": "external_1"
    },
      {
      "description": "Samsung Electric Company SAMSUNG 0x00000001",
      "workspaces": [
        "external_5",
        "external_6",
        "external_7",
        "external_8"
      ],
      "workspace_default": "external_5"
    }
    ]
    ```
2. Execute the script `change_monitor.py` with the path to the config as argument when starting hyprland
   and execute-once the listener with the path to the config as argument like this, with {path_to_repo}
   being the path to the repository
   ``` 
    exec-once = {path_to_repo}/monitors.sh {path_to_config}
    exec = python {path_to_repo}/change_monitor.py {path_to_config}
   ```