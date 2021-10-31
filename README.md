Ansible module steamcmd-install-game
=====================
This ansible module install and/or update any steamcmd available gamserver at a given location
This module have only been tested on Ubuntu LTS20.04

Pre-requisites
----------------
Ubuntu 20.04 LTS
steamcmd installed <https://developer.valvesoftware.com/wiki/SteamCMD>
python 3.X
Ansible 2.9+

Options
----------------
game_number : This is the AppID of the game server you want to install, you can find a list here <https://developer.valvesoftware.com/wiki/Dedicated_Servers_List>
game_location_path : Where will be installed the server game files, you must avec read and write access to the directory
steamcmd_path : Where is your steamcmd.sh installed 

Example Playbook
----------------

```
- name: "Install CS1.6 server on gamingserver"
  hosts: gamingserver
  gather_facts: no
  tasks:
    - name: "Install CS1.6"
      steamcmd_game_install:
        game_number: "90"
        game_location_path: "/home/user/games/cs"
        steamcmd_path: "/home/user/steamcmd/steamcmd.sh"
      register: resultat
```

Contribute & Contact
-----
To contribute follow ther guide at <https://github.com/firstcontributions/first-contributions>
Contact me at <git@hallynck.com>

License
-------

GNU GPLv3