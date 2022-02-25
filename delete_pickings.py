# -*- coding: utf-8 -*-

import rpc


def main():
    picks = rpc.search('stock.picking', [['state', '=', 'draft']])
    for p in picks:
        try:
            res = rpc.custom_method('stock.picking', 'unlink', [p])
            print(p, res)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
