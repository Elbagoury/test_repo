from openerp import models,fields

class sale_order_line(models.Model):

    _inherit = 'sale.order.line'

    remark = fields.Char("Remark")