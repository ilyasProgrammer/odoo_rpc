import rpc_prod as rpc


def main():
    prods = rpc.read('product.product', [['default_code', 'like', '_RM']], fields=['id', 'default_code'])
    for p in prods:
        if p['default_code'][-3:] == '_RM':
            atts = rpc.read('ir.attachment', [['res_model', '=', 'product.product'], ['res_id', '=', p['id']]], fields=['id','name'])
            for at in atts:
                if '_RM' not in at['name']:
                    rpc.custom_method('ir.attachment', 'unlink', [at['id']])
                    print('Deleted ', p, at)


if __name__ == "__main__":
    main()
