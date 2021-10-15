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
  steam_cmd:
    description: Location of the steamcmd binary
    required: yes
'''

EXAMPLES = '''
- name: "CSGO Install"
  steamcmd_game_install:
    game_number: "740"
    game_location: "/home/user-ansible/games/csgo"
    steam_cmd: "/usr/game/steamcmd"
'''

RETURN = '''
results:
    description: return installation status
    type: str
    returned: always
    sample: 'Install complete'
'''

import pysteamcmd
import os
import sys
import platform
import zipfile
import tarfile
import subprocess
from ansible.module_utils.basic import AnsibleModule
# urllib.urlretrieve no longer exists in python 3.
pythonVersion = sys.version_info[0]
if pythonVersion == 3:
    from urllib.request import urlretrieve
elif pythonVersion == 2:
    from urllib import urlretrieve

def main():
    module = AnsibleModule(
        argument_spec=dict(
            game_number=dict(required=True, type='str'),
            game_location_path=dict(required=True, type='str'),
            steam_cmd_path=dict(required=True, type='str'),
        )
    )

class Steamcmd(object):
    def __init__(self, install_path):
        """
        :param install_path: installation path for steamcmd
        """
        self.install_path = install_path
        if not os.path.isdir(self.install_path):
            raise SteamcmdException('Install path is not a directory or does not exist: {}'.format(self.install_path))

        self.platform = platform.system()
        if self.platform == 'Windows':
            self.steamcmd_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
            self.steamcmd_zip = 'steamcmd.zip'
            self.steamcmd_exe = os.path.join(self.install_path, 'steamcmd.exe')

        elif self.platform == 'Linux':
            self.steamcmd_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
            self.steamcmd_zip = 'steamcmd.tar.gz'
            self.steamcmd_exe = os.path.join(self.install_path, 'steamcmd.sh')

        else:
            raise SteamcmdException(
                'The operating system is not supported. Expected Linux or Windows, received: {}'.format(self.platform)
            )

    def _download_steamcmd(self):
        try:
            return urlretrieve(self.steamcmd_url, self.steamcmd_zip)
        except Exception as e:
            raise SteamcmdException('An unknown exception occurred! {}'.format(e))

    def _extract_steamcmd(self):
        if self.platform == 'Windows':
            with zipfile.ZipFile(self.steamcmd_zip, 'r') as f:
                return f.extractall(self.install_path)

        elif self.platform == 'Linux':
            with tarfile.open(self.steamcmd_zip, 'r:gz') as f:
                return f.extractall(self.install_path)

        else:
            # This should never happen, but let's just throw it just in case.
            raise SteamcmdException(
                'The operating system is not supported. Expected Linux or Windows, received: {}'.format(self.platform)
            )

    def _parse_vdf(self, vdf_path=None, vdf_data=None):
        if vdf_path and os.path.isfile(vdf_path):
            return vdf.parse(open(vdf_path))
        if vdf_data:
            return vdf.parse(vdf_data)
        return None

    def install(self, force=False):
        """
        Installs steamcmd if it is not already installed to self.install_path.
        :param force: forces steamcmd install regardless of its presence
        :return:
        """
        if not os.path.isfile(self.steamcmd_exe) or force is True:
            # Steamcmd isn't installed. Go ahead and install it.
            try:
                self._download_steamcmd()
            except SteamcmdException as e:
                return e

            try:
                self._extract_steamcmd()
            except SteamcmdException as e:
                return e
        else:
            raise SteamcmdException('Steamcmd is already installed. Reinstall is not necessary.'
                                    'Use force=True to override.')
        return

    def install_gamefiles(self, gameid, game_install_dir, user='anonymous', password=None, validate=False):
        """
        Installs gamefiles for dedicated server. This can also be used to update the gameserver.
        :param gameid: steam game id for the files downloaded
        :param game_install_dir: installation directory for gameserver files
        :param user: steam username (defaults anonymous)
        :param password: steam password (defaults None)
        :param validate: should steamcmd validate the gameserver files (takes a while)
        :return: subprocess call to steamcmd
        """
        if validate:
            validate = 'validate'
        else:
            validate = None

        steamcmd_params = (
            self.steamcmd_exe,
            '+login {} {}'.format(user, password),
            '+force_install_dir {}'.format(game_install_dir),
            '+app_update {}'.format(gameid),
            '{}'.format(validate),
            '+quit',
        )
        try:
            return subprocess.check_call(steamcmd_params)
        except subprocess.CalledProcessError:
            raise SteamcmdException("Steamcmd was unable to run. Did you install your 32-bit libraries?")

        try:
            return subprocess.check_call(steamcmd_params)
        except subprocess.CalledProcessError:
            raise SteamcmdException("Steamcmd was unable to run. Did you install your 32-bit libraries?")


    game_number_local = module.params.get('game_number')
    game_location_path_local = module.params.get('game_location_path')
    steam_cmd_path_local = module.params.get('steam_cmd')
    steamcmd = pysteamcmd.Steamcmd(steam_cmd_path_local)
    output_command = steamcmd.install_gamefiles(gameid=game_number_local, game_install_dir=game_location_path_local, user='anonymous', password=None, validate=True)
    output_command = str(output_command)

    if 'Sucess' in output_command:
        resultat = 'Install complete'
    else:
        resultat = 'Failed \n' + output_command

    module.exit_json(changed=False, results=resultat)


if __name__ == "__main__":
    main()
