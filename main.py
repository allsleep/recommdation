# -*- coding: utf-8 -*-
import sys

from data.collect import Collect

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv.count("-collect") > 0 or sys.argv.count("-c") > 0:
            Collect.main()
