Ansible module steamcmd-install-game
=====================
This ansible module install and/or update any steamcmd available gamserver at a given location\
This module have only been tested with bellow pre-requisites

Pre-requisites
----------------
Ubuntu 20.04 LTS\
Steamcmd installed <https://developer.valvesoftware.com/wiki/SteamCMD>\
Python 3.X\
Ansible 2.9+

Options
----------------
**game_id** : This is the AppID of the game server you want to install, list at the end of README.md\
**game_location_path** : Where will be installed the server game files, read and write right required to the directory\
**steamcmd_path** : Where your steamcmd.sh is installed

Example Playbook
----------------

```
- name: "Install CS1.6 server on gamingserver"
  hosts: gamingserver
  gather_facts: no
  tasks:
    - name: "Install CS1.6"
      steamcmd_game_install:
        game_id: "90"
        game_location_path: "/home/user/games/cs"
        steamcmd_path: "/home/user/steamcmd/steamcmd.sh"
      register: resultat
```

Contribute & Contact
-----
To contribute follow the guide at <https://github.com/firstcontributions/first-contributions>\
Contact me at <git@hallynck.com>  

License
-------

GNU GPLv3

Links
-------
List of AppID <https://developer.valvesoftware.com/wiki/Dedicated_Servers_List>
