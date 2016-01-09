from openerp import models, fields, api

class res_partner(models.Model):
    _inherit = 'res.partner'

    student = fields.Boolean('Student')
    faculty = fields.Boolean('Faculty')

    @api.multi
    def dummy_test(self):
        print "\n\n@@@@@@@@@###################testing from Partner"
        return True