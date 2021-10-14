#!/usr/bin/python

# Copyright: (c) 2021, LordTSK
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pysteamcmd
import os
from ansible.module_utils.basic import AnsibleModule

def main(): 
    module = AnsibleModule( 
        argument_spec=dict( 
            game_number    = dict(required=True, type='str'), 
            game_location_path    = dict(required=True, type='str'),
            steam_cmd_path    = dict(required=True, type='str'), 
        ) 
    )

game_number_local = module.params.get('game_number')
game_location_path_local = module.params.get('game_location_path')
steam_cmd_path_local = module.params.get('steam_cmd')


steamcmd = pysteamcmd.Steamcmd(steam_cmd_path_local)
output_command = steamcmd.install_gamefiles(gameid=game_number_local, game_install_dir=game_location_path_local, user='anonymous', password=None, validate=True)
output_command = str(output_command)

if 'Sucess' in output_command:
    resultat = 'Install complete'
else:
    resultat = 'Failed \n'+output_command

module.exit_json(changed=False, results=resultat) 

if __name__ == "__main__": 
    main()

DOCUMENTATION='''
module: steamcmd_game_install
author: Victor 
description: This module install any steamcmd available game as anonymous on a server with preinstalled steamcmd

options: 
  game_number: 
    description: Game ID in steamcmd https://developer.valvesoftware.com/wiki/Dedicated_Servers_List
    required: yes 
  game_location_path: 
    description: Where the game server file will be stored
    required: yes 
  steam_cmd: 
    description: Location of the steamcmd binary
    required: yes 
'''

EXAMPLES='''
- name: "CSGO Install" 
  steamcmd_game_install: 
    game_number: "740" 
    game_location: "/home/user-ansible/games/csgo"
    steam_cmd: "/usr/game/steamcmd" 
'''

RETURN = '''
results: 
    description: return installation status
'''