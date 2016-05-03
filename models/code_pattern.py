import ipdb as pdb
from openerp import models, fields

class code_pattern (models.Model):
    _name = "code.pattern"

    prod = fields.Many2one('product.template')
    name_att_val = fields.Many2one('product.attribute.value')
    code = fields.Char('code_reff', default='00')