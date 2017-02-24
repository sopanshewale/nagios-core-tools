#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import statvfs
from sys import exit
from optparse import OptionParser


def measurePartionUsage(partition):
    p_details = statvfs(partition)
    totalBytes = float(p_details.f_bsize * p_details.f_blocks)
    totalUsedSpace = float(p_details.f_bsize * (p_details.f_blocks
                           - p_details.f_bfree))
    totalAvailSpace = float(p_details.f_bsize * p_details.f_bfree)
    return {'used': '%.2f' % float(totalUsedSpace / 1024 / 1024
            / 1024), 'total': '%.2f' % float(totalBytes / 1024 / 1024
            / 1024), 'free': '%.2f' % float(totalAvailSpace / 1024
            / 1024 / 1024)}


def handleAlert(
    warn,
    crit,
    details,
    partition,
    ):
    percentage_free = float(details['free']) / float(details['total'])
    percentage_free = '%.2f' % float(percentage_free * 100.0)
    percentage_used = float(details['used']) / float(details['total'])
    percentage_used = '%.2f' % float(percentage_used * 100.0)

    if float(percentage_free) < float(crit):
        print 'CRITICAL: ' + partition + ':  total ' \
            + str(details['total']) + 'GB, used ' + str(details['used'
                ]) + 'GB (' + str(percentage_used) + '%), free ' \
            + str(details['free']) + 'GB (' + str(percentage_free) \
            + '%)|Used Space=' + str(float(details['used']) * 1024) + 'MB;;;;' + str(float(details['total'])*1024) + ';'
        exit(2)
    if float(percentage_free) < float(warn):
        print 'WARNING: ' + partition + ':  total ' \
            + str(details['total']) + 'GB, used ' + str(details['used'
                ]) + 'GB (' + str(percentage_used) + '%), free ' \
            + str(details['free']) + 'GB (' + str(percentage_free) \
            + '%)|Used Space=' + str(float(details['used']) * 1024) + 'MB;;;;' + str(float(details['total'])*1024) + ';'
        exit(1)

    print 'OK: ' + partition + ':  total ' + str(details['total']) \
        + 'GB, used ' + str(details['used']) + 'GB (' \
        + str(percentage_used) + '%), free ' + str(details['free']) \
        + 'GB (' + str(percentage_free) + '%)|Used Space=' + str(float(details['used']) * 1024) + 'MB;;;;' + str(float(details['total'])*1024) + ';'
    exit(0)


def verifyArguments(options):
    if float(options.warning) <= float(options.critical):
        print 'UNKNOWN: You can not have critical options bigger than warnings'
        exit(3)


def main():
    parser = OptionParser(usage='usage: %prog [options] filename',
                          version='%prog 1.0')
    parser.add_option(
        '-w',
        '--warning',
        action='store',
        type='int',
        dest='warning',
        help='Please Provide warning parameter, which is percentage of free space'
            ,
        )

    parser.add_option(
        '-c',
        '--critical',
        action='store',
        type='int',
        dest='critical',
        help='Please Provide critical parameter, which is percentage of free space'
            ,
        )

    parser.add_option(
        '-p',
        '--partition',
        action='store',
        type='string',
        dest='partition',
        help='Please Provide partition name',
        )

    try:
        (options, args) = parser.parse_args()
    except:
        parser.print_help()
        exit(0)
    verifyArguments(options)
    details = measurePartionUsage(options.partition)
    handleAlert(options.warning, options.critical, details,
                options.partition)


if __name__ == '__main__':
    main()

