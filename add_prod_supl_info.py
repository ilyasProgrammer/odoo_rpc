# import rpc_local as rpc
import rpc_stag as rpc


def main():
    products = rpc.search('product.template', [['active', '=', True], ['seller_ids', '!=', False]])
    for prod in products:
        psys = rpc.search_read('product.supplierinfo', [['product_tmpl_id', '=', prod]])
        if len(psys) > 0:
            first = min(psys, key=lambda x: x['sequence'])
            partner = rpc.read('res.partner', [first['name'][0]])
            if len(partner) > 0 and partner[0]['category_vendor_id']:
                vals = {
                    'name': partner[0]['category_vendor_id'][0],
                    'product_tmpl_id': prod,
                    'sequence': -1
                }
                new_psy = rpc.create('product.supplierinfo', vals)
                print('product ', prod, ' new psy ', new_psy)
                # for psy in psys:
                #     res = rpc.write('product.supplierinfo', psy['id'], {'sequence': psy['sequence'] + 1})
                #     print('updated ', psy['id'])


if __name__ == "__main__":
    main()
