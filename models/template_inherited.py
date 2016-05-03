import ipdb as pdb
from openerp import models, fields, api
import operator

class product_template(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    referencia_fabricante = fields.Char('reff_fabri')
    code_pattern = fields.One2many('code.pattern','prod',string='Code Pattern')

    @api.one
    def compute_values(self):
        lista_prod = self.product_variant_ids.ids
        final ={}
        for x in lista_prod:
            prod = self.env['product.product'].browse(x)
            lista_val = prod.attribute_value_ids.ids
            for y in lista_val:
                value = self.env['product.attribute.value'].browse(y)
                final[value.id] = 1
        #pdb.set_trace()
        for la_id in final.keys():
            valor = self.env['product.attribute.value'].browse(la_id)
            print valor.name
            code_create = self.env['code.pattern']
            if not code_create.search([('name_att_val','=',valor.id)]):
                code_create.create({
                'prod':self.id,
                'name_att_val':valor.id
                })

    @api.one
    def compute_codes(self):
        lista_prod = self.product_variant_ids.ids
        for x in lista_prod:
            order = {}
            prod = self.env['product.product'].browse(x)
            lista_val = prod.attribute_value_ids.ids
            code = self.referencia_fabricante or ''
            #pdb.set_trace()
            for y in lista_val:
                #pdb.set_trace()
                value = self.env['product.attribute.value'].browse(y)
                order[value] = value.attribute_id.id
            sorted_order = sorted(order.items(), key=operator.itemgetter(1))
            for att in sorted_order:
                char_att = self.code_pattern.search([('name_att_val','=',att[0].id),('prod','=',self.id)]).code
                code += char_att
            prod.codigo_venta = code






class product_product(models.Model):
    _name="product.product"
    _inherit="product.product"

    codigo_venta = fields.Char('Codigo de producto',default="00")