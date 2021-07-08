# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Flybreak
#
# SPDX-License-Identifier: Apache-2.0
#
# Change Logs:
# Date           Author       Notes
# 2021-06-06     flybreak     the first version
#
import argparse
import os
import sys
import logging
import time
import json
import requests

LOG_LVL = logging.INFO

def determine_url_valid(url_from_srv):
    """Check the validity of urls."""

    # check url is github
    if not url_from_srv.startswith("https://github.com"):
        logging.warning("not support url: {}".format(url_from_srv))
        return False

    headers = {'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip, deflate',
               'Accept': '*/*',
               'User-Agent': 'curl/7.54.0'}

    try:
        for i in range(0, 3):
            r = requests.get(url_from_srv, stream=True, headers=headers)
            if r.status_code == requests.codes.not_found:
                if i == 2:
                    logging.warning("Warning : %s is invalid." % url_from_srv)
                    return False
                time.sleep(1)
            else:
                break

        return True

    except Exception as e:
        logging.error('Error message:%s\t' % e)
        logging.error('Network connection error or the url : %s is invalid.\n' %
              url_from_srv)


def get_json_info(json_pathname):
    with open(json_pathname, 'r+') as f:
        json_content = f.read()

    try:
        package_info = json.loads(json_content)
    except ValueError:
        logging.error('The JSON config file syntax checking failed!')
        return False

    return package_info


def file_path_check(package_info, pathname):
    info_dir = os.path.dirname(pathname)

    if package_info['name'] == os.path.basename(info_dir):
        return True
    else:
        logging.debug("===========================================>")
        logging.error("Error: package name is different with package folder name.")
        logging.debug(pathname)
        logging.error("package name:%s" % package_info['name'])
        logging.debug("package folder name: %s" % os.path.basename(info_dir))
        return False


def check_json_file(work_root):
    """Check the json file."""

    file_count = 1
    folder_walk_result = os.walk(work_root)

    for path, d, file_list in folder_walk_result:
        for filename in file_list:
            if filename == 'package.json':
                json_pathname = os.path.join(path, 'package.json')
                json_info = get_json_info(json_pathname)
                logging.debug("\nNo.%d" % file_count)
                file_count += 1
                if not json_file_content_check(json_info):
                    return False

                if not file_path_check(json_info, json_pathname):
                    return False

    return True


def json_file_content_check(package_info):
    """Check the content of json file."""

    if package_info['category'] == '':
        logging.warning('The category of ' + package_info['name'] + ' package is lost.')
        return False

    if 'enable' not in package_info or package_info['enable'] == '':
        logging.warning('The enable of ' + package_info['name'] + ' package is lost.')
        return False

    if package_info['author']['name'] == '':
        logging.warning('The author name of ' + package_info['name'] + ' package is lost.')
        return False

    if package_info['author']['email'] == '':
        logging.warning('The author email of ' + package_info['name'] + ' package is lost.')
        return False

    if package_info['license'] == '':
        logging.warning('The license of ' + package_info['name'] + ' package is lost.')
        return False

    if package_info['repository'] == '':
        logging.warning('The repository of ' + package_info['name'] + ' package is lost.')
        return False
    else:
        if not determine_url_valid(package_info['repository']):
            return False

    for i in range(0, len(package_info['site'])):
        package_version = package_info['site'][i]['version']
        package_url = package_info['site'][i]['URL']
        logging.debug("%s : %s" % (package_version, package_url))
        if not package_url[-4:] == '.git':
            logging.debug(package_info['site'][i]['filename'])
        if not determine_url_valid(package_url):
            return False

    return True


class Bear:
    def __init__(self):
        return

    def check(self, pkg_index_path):
        logging.debug('bear check package')
        return check_json_file(pkg_index_path)

    def build(self, bsp_path, pkg_path):
        logging.debug('bear build package')
        # os.environ['RTT_ROOT'] = r'E:\0Workspace\github\rt-thread'
        os.environ['BEAR_PKG_ROOT'] = os.path.abspath(pkg_path)

        logging.debug("RTT_ROOT={}".format(os.getenv('RTT_ROOT')))
        logging.debug("BEAR_PKG_ROOT={}".format(os.getenv('BEAR_PKG_ROOT')))
        if os.system('scons --directory=' + bsp_path + ' -j12 -s') != 0:
            logging.error('build failed! pkg_path:[{}]'.format(pkg_path))
            return False
        success = True
        return success

    def test(self):
        logging.debug('bear test package')
        success = True
        return success

    def config(self, rtt_root, toolchain_path):
        logging.debug('bear config self,rtt_root:{},toolchain_path:{}'.format(rtt_root, toolchain_path))

# sub-command functions
def fun_check(args):
    logging.debug('check package,pkg_path:{},pkg_index_path:{}'.format(args.pkg_path, args.pkg_index_path))
    bear = Bear()
    bear.check(args.pkg_index_path)

def fun_build(args):
    logging.debug('build package with {},pkg_path:{},pkg_index_path:{}'.format(args.bsp, args.pkg_path, args.pkg_index_path))
    bear = Bear()
    # bear.check()
    if bear.build(args.bsp, args.pkg_path) == False:
        sys.exit(-1)

def fun_test(args):
    logging.debug('test package with {},pkg_path:{},pkg_index_path:{}'.format(args.bsp, args.pkg_path, args.pkg_index_path))
    bear = Bear()
    # bear.check()
    if bear.build(args.bsp, args.pkg_path) == False:
        sys.exit(-1)
    bear.test()

def fun_config(args):
    logging.debug('config bear,rtt_root:{},toolchain_path:{}'.format(args.rtt_root, args.toolchain_path))
    bear = Bear()
    bear.config(args.rtt_root, args.toolchain_path)

def main():
    logging.basicConfig(level=LOG_LVL, format='%(asctime)s %(levelname)s: %(message)s', datefmt=None)
    parser = argparse.ArgumentParser(description='An RT-Thread software package assisted development tool.', prog=os.path.basename(sys.argv[0]))

    subparsers = parser.add_subparsers(help='sub-command help')
    # create the parser for the "check" command
    parser_sub = subparsers.add_parser('check', help='Check the package format and code style')
    parser_sub.add_argument('--pkg_path', metavar='pkg_path', help='the package path', default=".")
    parser_sub.add_argument('--pkg_index_path', metavar='pkg_index_path', help='the package index path', default="./package")
    parser_sub.add_argument('--bsp', metavar='bsp_name', help='the bsp for build package', default="qemu-vexpress-a9")
    parser_sub.set_defaults(func=fun_check)

    # create the parser for the "build" command
    parser_sub = subparsers.add_parser('build', help='build the package with qemu-vexpress-a9')
    parser_sub.add_argument('--pkg_path', metavar='pkg_path', help='the package path', default=".")
    parser_sub.add_argument('--pkg_index_path', metavar='pkg_index_path', help='the package index path', default="./package")
    parser_sub.add_argument('--bsp', metavar='bsp_name', help='the bsp for build package', default="qemu-vexpress-a9")
    parser_sub.set_defaults(func=fun_build)

    # create the parser for the "test" command
    parser_sub = subparsers.add_parser('test', help='test the package')
    parser_sub.add_argument('--pkg_path', metavar='pkg_path', help='the package path', default=".")
    parser_sub.add_argument('--pkg_index_path', metavar='pkg_index_path', help='the package index path', default="./package")
    parser_sub.add_argument('--bsp', metavar='bsp_name', help='the bsp for build package', default="qemu-vexpress-a9")
    parser_sub.set_defaults(func=fun_test)

    # create the parser for the "test" command
    parser_sub = subparsers.add_parser('config', help='config bear')
    parser_sub.add_argument('--rtt_root', metavar='path', help='the RTT ROOT path', default="./rt-thread")
    parser_sub.add_argument('--toolchain_path', metavar='path', help='the toolchain path', default=".")
    parser_sub.set_defaults(func=fun_config)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
