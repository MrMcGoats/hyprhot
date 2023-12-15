import argparse
import os
from dataclasses import dataclass
import json
import argparse
import logging

logger = logging.getLogger('Hyprhot')
logger.setLevel(logging.INFO)

@dataclass
class MonitorInfo:
    description: str
    workspaces: [str]
    workspace_default: str


def get_monitors():
    stream = os.popen('hyprctl monitors -j')
    return json.loads(stream.read())


def get_workspaces():
    stream = os.popen('hyprctl workspaces -j')
    return json.loads(stream.read())


def parse_config(path_config):
    with open(path_config) as f:
        config_parsed = json.load(f)

    return [MonitorInfo(**info_monitor) for info_monitor in config_parsed]


def move_workspace_to_monitor(workspace, monitor):
    os.system(
        f'hyprctl dispatch moveworkspacetomonitor name:{workspace} {monitor["name"]}'
    )

def show_workspace_on_monitor(workspace, monitor):
    os.system(f'hyprctl dispatch focusmonitor {monitor["name"]}')
    os.system(f'hyprctl dispatch workspace name:{workspace}')



parser = argparse.ArgumentParser(
    'Monitor Switcher',
    description='Assign workspaces to monitors based on configured assignments on hyprland.'
                'Handle multiple monitors (e.g. on different physical locations like office and home) '
                'being assigned to the same workspace. '
                'Also ensure that workspaces are moved to their assigned monitor in case they'
                'were assigned to the wrong monitor before, which is common when hot-plugging.'
)
parser.add_argument(
    'path_config',
    type=str,
    help='Path to a .json config file. '
         'Content is a list of dicts. Each dict represents the configuration of a monitor and has the following keys:\n'
         '- description: monitor description that can be used in a hyprland workspace rule to identify the monitor \n'
         '- workspaces: list of workspace names (strings) the monitor is assigned to\n'
         '- workspace_default: string with the monitors default workspace name from workspaces.'
)

args = parser.parse_args()
rules = parse_config(args.path_config)
monitors = get_monitors()

for monitor in monitors:
    for rule in rules:
        # check if description is in monitor's description instead of equality
        #   because descriptions yielded by hyprctl contain also connection port
        # TODO: do comparison in more sophisticated way than with substring
        #   to avoid false-positives due to similar descriptions
        if rule.description in monitor['description']:
            # Apply workspace rules to assign the workspaces to the monitor
            for workspace in rule.workspaces:
                workspace_rule = f'workspace name:{workspace},monitor:desc:{rule.description}{",default:true" if rule.workspace_default == workspace else ""}'
                os.system(f'hyprctl keyword {workspace_rule}')

            # Move all workspaces that are assigned to the monitor to the monitor.
            #   in order to handle the case of hotplugging, where some workspaces may already be displayed on another
            #   monitor
            workspaces_existing = get_workspaces()
            for workspace_existing in workspaces_existing:
                if workspace_existing['name'] in rule.workspaces:
                    if workspace_existing['monitor'] != monitor['name']:
                        logger.info(
                            f'Workspace {workspace_existing["name"]} should be assigned to monitor {monitor["name"]}, '
                            f'but is assigned to monitor {workspace_existing["monitor"]}. Reassigning.')
                    move_workspace_to_monitor(workspace_existing['name'], monitor)

            # set the monitor's current workspace to the default one if the monitor's current workspace
            #   is not in the monitor's assigned workspaces
            monitors_current = get_monitors()
            for monitor_current in monitors_current:
                if rule.description in monitor_current['description']:
                    if monitor_current['activeWorkspace']['name'] not in rule.workspaces:
                        logger.info(
                            f'Monitor {monitor_current["description"]} has invalid workspace {monitor_current["activeWorkspace"]["name"]}. switching to default {rule.workspace_default}')
                        show_workspace_on_monitor(rule.workspace_default, monitor_current)
