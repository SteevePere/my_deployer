#!/usr/bin/env python3
"""SSH client"""

import sys
import time
import datetime
import paramiko
import logging
from termcolor import colored

# custom modules
import globals

logging.basicConfig(filename=globals.LOG_FILE, level=logging.DEBUG)  # logger config


def ssh_connect(args):
    """Connects to remote server via SSH"""

    server = args.server
    user = args.user
    password = globals.REMOTE_SSH_PASSWORD
    now = datetime.datetime.now()  # for logger history

    ssh = paramiko.SSHClient()  # setting up client
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(server, username=user, password=password)

    except:
        print(colored("ERROR: SSH connection to " + server + " failed", 'red'))
        sys.exit(1)

    print(colored("\n--- SSH connection to " + server + " successful ---", 'yellow'))
    logging.info('\n')
    logging.info('NEW RUN ' + str(now) + '\n')

    return(ssh)


def ssh_command(ssh, command, print_stdout):
    """Sends Unix commands to remote server via SSH"""

    stdin, stdout, stderr = ssh.exec_command(command)
    stdout_output = stdout.readlines()  # retrieving standard output
    stderr_output = stderr.readlines()  # retrieving error output

    standard_output = ""
    error_output = ""

    if (stderr_output):

        for line in stderr_output:
            error_output += line

        print(colored(error_output, 'red'))
        logging.warning(error_output + 'status: K.O.')

    if (print_stdout):  # boolean passed to toggle output printout

        for line in stdout_output:
            standard_output += line

        print(standard_output)
        logging.info(standard_output + 'status: O.K.')

    return(stdout_output)


def ssh_close(ssh):
    """Closes SSH connection to remote server"""

    ssh.close()
    print(colored("\n--- SSH connection closed ---", 'yellow'))

    return
