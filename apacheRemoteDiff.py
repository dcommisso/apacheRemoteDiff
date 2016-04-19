#!/usr/bin/env python

from fabric.api import env, run
from fabric.tasks import execute
from fabric.context_managers import hide
import argparse
import re
import difflib

descrizione = "Tool per diff tra file su server remoti. E' ottimizzato per Apache: ignora le linee vuote, l'identazione, i commenti, le tabulazioni, gli spazi multipli, gli spazi alla fine della riga e le occorrenze degli indirizzi IP del server. I file confrontati, se non esplicitamente specificato, sono: /etc/httpd/conf/httpd.conf, etc/httpd/conf.d/ssl.conf, /etc/httpd/conf.d/workers.properties"

parser = argparse.ArgumentParser(description=descrizione)
parser.add_argument('hosts', help='lista dei nodi apache separati da virgola', metavar='host1,host2')
parser.add_argument('-u', default='root', metavar='username', help="username per connettersi alle macchine remote")
parser.add_argument('-p', metavar='password', help="password per connettersi alle macchine remote")
parser.add_argument('--configfiles', default='/etc/httpd/conf/httpd.conf,/etc/httpd/conf.d/ssl.conf,/etc/httpd/conf.d/workers.properties',\
                    help='lista file da confrontare separati da virgola', metavar='file1,file2,file3,...')
parser.add_argument('--reportok', action='store_true', help='restituisce "OK" se non ci sono differenze, invece di nessun output')
args = parser.parse_args()

env.hosts = args.hosts.split(',')
env.user = args.u

if args.p:
    env.password = args.p

def remotecat(configfile):
    return run('cat %s' % configfile)

def purgeip(configfile):
    ''' elimina gli indirizzi IP del server dal file di configurazione'''
    own_ip_regexp = re.compile(r'listen\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', flags=re.IGNORECASE)
    own_ip_list = own_ip_regexp.findall(configfile)
    for ip in own_ip_list:
        configfile = configfile.replace(ip, '')
    return configfile

def purgehostname(configfile, hostname):
    ''' ricava l'hostname senza dominio e toglie tutte le occorrenze nella stringa in input '''
    hostname_rule = re.compile(r'(\w+)\..*')
    hostname_no_domain = hostname_rule.sub(r'\1', hostname)
    return re.sub(hostname_no_domain, '', configfile, flags = re.IGNORECASE)

def purgejunk(configfile):
    ''' elimina linee vuote, identazione, commenti, tabulazioni, spazi multipli e spazi alla fine'''
    blank_line_rule = re.compile(r'^\s+', flags = re.MULTILINE)
    comments_rule = re.compile(r'^\s*#.*', flags = re.MULTILINE)
    tabs_rule = re.compile(r'\t+')
    spaces_rule = re.compile(r' +')
    configfile = comments_rule.sub('', configfile)
    configfile = blank_line_rule.sub('', configfile)
    configfile = tabs_rule.sub(' ', configfile)
    configfile = spaces_rule.sub(' ', configfile)
    retfile = ''
    for line in configfile.split('\n'):
        retfile += line.rstrip() + '\n'
    return retfile

def compare_strings_in_dict(remote_files_dict, configFileName):
    '''confronta due stringhe in un dizionario restituito da fabric execute in input, facendo preventivamente purge e restituisce le eventuali differenze'''
    hostname1, hostname2 = remote_files_dict.keys()
    a, b = remote_files_dict.values()
    first_file_desc = configFileName + ' - ' + hostname1
    second_file_desc = configFileName + ' - ' + hostname2

    a = purgejunk(a)
    a = purgeip(a)
    a = purgehostname(a, hostname1)

    b = purgejunk(b)
    b = purgeip(b)
    b = purgehostname(b, hostname2)

    diff_result = difflib.unified_diff(a.split('\n'),b.split('\n'), fromfile=first_file_desc, tofile=second_file_desc)
    return '\n'.join(diff_result)
    
if __name__ == '__main__':
    report = ''
    for configfile in args.configfiles.split(','):
        with hide('everything'):
            remote_files_dict = execute(remotecat, configfile)
            differences = compare_strings_in_dict(remote_files_dict, configfile)
            if differences:
                report += differences
    if not report and args.reportok:
        print('OK')
    else:
        print(report)

