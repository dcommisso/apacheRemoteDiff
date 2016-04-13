#!/usr/bin/env python

from fabric.api import env, run
from fabric.tasks import execute
from fabric.context_managers import hide
import argparse
import re

parser = argparse.ArgumentParser(description='tool per controllare se i file di configurazione di due Apache in cluster sono allineati')
parser.add_argument('hosts', help='lista dei nodi apache separati da virgola', metavar='host1,host2')
parser.add_argument('-u', default='root', metavar='username', help="username per connettersi alle macchine remote")
parser.add_argument('-p', metavar = 'password', help="password per connettersi alle macchine remote")
parser.add_argument('--configfiles', default='/etc/httpd/conf/httpd.conf,/etc/httpd/conf.d/ssl.conf,/etc/httpd/conf.d/workers.properties',\
                    help='lista file da confrontare separati da virgola')
args = parser.parse_args()

env.hosts = args.hosts.split(',')
env.user = args.u

if args.p:
    env.password = args.p

def remotecat(configfile):
    return run('cat %s' % configfile)

def purgeip(configfile):
    ''' elimina l'indirizzo IP del server dal file di configurazione'''
    own_ip_regexp = re.compile(r'listen\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', flags=re.IGNORECASE)
    try:
        own_ip = own_ip_regexp.search(configfile).group(1)
        return configfile.replace(own_ip, '')
    except AttributeError:
        return configfile

if __name__ == '__main__':
    files_list = []
    for configfile in args.configfiles.split(','):
        with hide('everything'):
            files_list.append(execute(remotecat, configfile))
    print purgeip((files_list[1]['RT-GIUSTIZIA-FE01-P1.rt.tix.it']))
