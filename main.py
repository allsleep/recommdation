# -*- coding: utf-8 -*-
import sys

from data.collect import Collect

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv.count("-collect") or sys.argv.count("-c") > 1:
            Collect.main()
