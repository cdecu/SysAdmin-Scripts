#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Doc !
"""

import argparse
import os.path
import pysftp

__author__ = 'cdc'
__email__ = 'cdc@xpertbilling.com'
__version__ = '0.1.9'

cinfo = {'host': '', 'username': '', 'password': '', 'port': 2222}


def sftpConnect():
    """
    Just Test connection to host
    """
    print('Connection to', cinfo['host'])
    with pysftp.Connection(**cinfo):
        print('..Connected')
    # connection closed automatically at the end of the with-block
    print('..Disconnected')
    return True


def sftpListDir(d):
    """
    Just Test connection to host and list wanted dir
    """
    print('..Connection to', cinfo['host'])
    with pysftp.Connection(**cinfo) as sftp:
        print('..List Dir ', d)
        with sftp.cd(d):
            ld = sftp.listdir()
    # connection closed automatically at the end of the with-block
    print('..Disconnected')
    return ld


def sftpUpload(localFile, targetDir):
    """
    Just Test connection to host and upload localFile to targetDir
    """
    if os.path.isfile(localFile):
        print('..Connection to', cinfo['host'])
        with pysftp.Connection(**cinfo) as sftp:
            print('..Chg to Dir ', targetDir)
            with sftp.cd(targetDir):
                targetFile = os.path.basename(localFile)
                if not sftp.isfile(targetFile):
                    print('..Upload <', localFile, '> to <', targetDir, '>', targetFile)
                    sftp.put(localFile)
                    uploaded = True
                else:
                    print('**Remote File', targetFile, 'allready exists')
                    uploaded = False
                    # connection closed automatically at the end of the with-block
            print('..Disconnected')
        return uploaded
    else:
        print('**File', localFile, 'not Found')
        return False


""" ********************************************************************************************************************
Start Upload  files
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SFTPUpload.py",
        description='SFTP Upload script for Isirnet',
        epilog="\nbe carefull and good lock !\n",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80)
        )
    parser.add_argument('--host', help='Remote Server Address', type=str, default='xpbnas.myDS.me', required=False)
    parser.add_argument('--port', help='Remote Server Port', type=int, default=2222, required=False)
    parser.add_argument('--user', help='User Name', type=str, default='cdc', required=False)
    parser.add_argument('--pwd', help='User Password', type=str, default='338833', required=False)
    parser.add_argument('-s', '--source', help='Full File Name to upload', type=str, default='Test.py', required=False)
    parser.add_argument('-t', '--target', help='Remote Folder', type=str, default='Tempo', required=False)
    args = parser.parse_args()
    parser.print_help()
    print()
    cinfo['host'] = args.host
    cinfo['port'] = args.port
    cinfo['username'] = args.user
    cinfo['password'] = args.pwd
    print('Start Upload', args.source, 'to', args.host, args.target)
    if sftpUpload(args.source, args.target):
        print('Ok')
        exit(0)
    print('Error')
    exit(1)

""" ********************************************************************************************************************
Sample Test and Usage not called after main !
"""

# Test sftpConnect
if sftpConnect():
    print('Ok')
print()

# Test sftpListDir
listDir = sftpListDir('Tempo')
print(listDir)
print()

# Test sftpUpload
if sftpUpload('/home/cdc/Téléchargements/git4.jpg', 'Tempo'):
    print('Ok')
else:
    print('Err')
print('')

# Test sftpListDir
listDir = sftpListDir('Tempo')
print(listDir)

parser = argparse.ArgumentParser(prog="SFTPUpload.py", description='SFTP Upload script for Isirnet',
                                 usage="%(prog)s [options]")
