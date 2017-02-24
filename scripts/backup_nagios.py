#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import tarfile
import os

backup_dir = 'backup'
data_dirs = ['data', 'data2', 'data3']
data_files = ['/home/vagrant/shellscripts/1.sh', ]


def create_todays_backup(dirs, files, destination):
    backup_name = os.path.join(destination, today() + '.tar.gz')

    # # delete only if last backup with same day name exist ##

    if os.path.exists(backup_name):
        try:
            print 'Removing Old Copy: ' + backup_name
            os.remove(backup_name)
        except OSError, e:
            print 'Error: %s - %s.' % (e.backup_name, e.strerror)

    print 'Creating new backup: ' + backup_name
    tar = tarfile.open(backup_name, 'w:gz')
    for directory in dirs:
        tar.add(directory)
    for file in files:
        tar.add(file)

    tar.close()
    print 'Writing ' + backup_name + ' complete'
    print 'Backup up  - DONE'


def today():
    now = datetime.datetime.now()
    return now.strftime('%A').lower()


def main():

    # check existance of backup directory

    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    absolute_dirs = []
    for dir in data_dirs:
        data_d = [os.path.join(dir, name) for name in os.listdir(dir)
                  if os.path.isdir(os.path.join(dir, name))]
        absolute_dirs = absolute_dirs + data_d

    # print absolute_dirs

    create_todays_backup(absolute_dirs, data_files, backup_dir)


if __name__ == '__main__':
    main()

