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
  steamcmd_path:
    description: Steamcmd binary path
    required: yes
'''

EXAMPLES = '''
- name: "CSGO Install"
  steamcmd_game_install:
    game_number: "740"
    game_location_path: "/home/steamserver/csgoserver"
    steamcmd_path: ""/home/steamserver/steamcmd/steamcmd.sh"
'''

RETURN = '''
results:
    description: return installation status
    type: str
    returned: always
    sample: 'Install complete'
'''

import os
import pty
import subprocess
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            game_number=dict(required=True, type='str'),
            game_location_path=dict(required=True, type='str'),
            steamcmd_path=dict(required=True, type='str'),
        )
    )

    game_number_local = module.params.get("game_number")
    game_location_path_local = module.params.get("game_location_path")
    steamcmd_path_local = module.params.get("steamcmd_path")
#Steamcmd call with argumentss
    output = ''
    command = steamcmd_path_local+' +login anonymous +app_update '+game_number_local+' +force_install_dir '+game_location_path_local+' +quit'
    master, slave = pty.openpty()
    p=subprocess.Popen(command.split(), stdout=slave)
    os.close(slave)
#?Retriveing output stream and use conditions to get results
    while True:
        try:
             # read in a chunk of data
             data = os.read(master, 1024)
             output += data.decode('ascii')
             for line in output.splitlines():
                 if "Success!" in line:
                     resultat = "Install successfull"
                     module.exit_json(changed=True, results=resultat)
                 else:
                     resultat = "Install failed"
        except OSError as e:
            module.fail_json(msg=resultat)

if __name__ == "__main__":
    main()
