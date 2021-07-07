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

LOG_LVL = logging.DEBUG

class Bear:
    def __init__(self):
        return

    def check(self):
        logging.debug('bear check package')
        check_ok = True
        return check_ok

    def build(self, bsp_path, pkg_path):
        logging.debug('bear build package')
        # os.environ['RTT_ROOT'] = r'E:\0Workspace\github\rt-thread'
        os.environ['BEAR_PKG_ROOT'] = pkg_path

        logging.debug(os.getenv('RTT_ROOT'))
        if os.system('scons --directory=' + bsp_path + ' -j12') != 0:
            logging.error('build failed! pkg_path:[{}]'.format(pkg_path))
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
    bear.check()

def fun_build(args):
    logging.debug('build package with {},pkg_path:{},pkg_index_path:{}'.format(args.bsp, args.pkg_path, args.pkg_index_path))
    bear = Bear()
    bear.check()
    bear.build(args.bsp, args.pkg_path)

def fun_test(args):
    logging.debug('test package,pkg_path:{},pkg_index_path:{}'.format(args.pkg_path, args.pkg_index_path))
    bear = Bear()
    bear.check()
    bear.build()
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
