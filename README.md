Ansible module steamcmd-install-game
=====================
This ansible module install any steamcmd available gamserver

Example Playbook
----------------

```
- name: "Install CS1.6 on steamserver"
  hosts: steamserver
  gather_facts: no
  tasks:
    - name: "Install CS1.6"
      steamcmd_game_install:
        game_number: "90"
        game_location_path: "/home/steamserver/games/cs"
        steamcmd_path: "/home/steamserver/steamcmd/steamcmd.sh"
      register: resultat
```

License
-------

GNU GPLv3

Links
-----

<https://developer.valvesoftware.com/wiki/SteamCMD>
<https://github.com/wmellema/Py-SteamCMD-Wrapper>
<https://developer.valvesoftware.com/wiki/Dedicated_Servers_List>
