from openerp import workflow
from openerp import models, fields, api

class wiz_reject_reason(models.TransientModel):
    _name = 'wiz.reject.reason'

    name = fields.Text('Reason', required=True)

    @api.multi
    def action_reject(self):
        student_obj = self.env['student.student']
        cr, uid, context = self.env.args
        print "\n\ncontext###    ", context
        for rec in self:
            student = student_obj.browse(context['active_id'])
            student.write({'note': rec.name})
            workflow.trg_validate(uid, 'student.student', context['active_id'], 'register_reject', cr)
        return True