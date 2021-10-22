#!/usr/bin/python

# Copyright: (c) 2021, LordTSK
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
module: steamcmd_game_install
author:
  - Victor (@LordTSK)
description: This module install any steamcmd available game as anonymous on a server with preinstalled steamcmd
short_description: Installing steam game servers
version_added: 1.0

options:
  game_number:
    description: Game ID in steamcmd https://developer.valvesoftware.com/wiki/Dedicated_Servers_List
    required: yes
  game_location_path:
    description: Where the game server file will be stored
    required: yes
'''

EXAMPLES = '''
- name: "CSGO Install"
  steamcmd_game_install:
    game_number: "740"
'''

RETURN = '''
results:
    description: return installation status
    type: str
    returned: always
    sample: 'Install complete'
'''

import os
from pysteamcmdwrapper import SteamCMD
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            game_number=dict(required=True, type='str'),
            game_location_path=dict(required=True, type='str'),
        )
    )

    game_number_local = module.params.get("game_number")
    game_location_path_local = module.params.get("game_location_path")
    
    s = SteamCMD("steamcmd")
    output_command = str(s.app_update(game_number_local,os.path.join(os.getcwd(),game_location_path_local),validate=True))

    if 'Success!' in output_command:
        resultat = 'Install complete'
        module.exit_json(results=resultat)
    else:
        resultat = 'Failed'

if __name__ == "__main__":
    main()