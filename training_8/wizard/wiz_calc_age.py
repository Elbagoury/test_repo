from datetime import datetime
from openerp import models, fields, api

class wiz_calc_age(models.TransientModel):
    _name = 'wiz.calc.age'

    from_date = fields.Date('From Date', required=True)
    to_date = fields.Date('To Date', required=True)

    # v7 code just for comparison
    def calc_x(self, cr, uid, ids, context=None):
        student_obj = self.pool.get('student.student')
        for rec in self.browse(cr, uid, ids, context=context):
            rec
            student_ids = student_obj.search(cr, uid, [('dob', '>=', rec.from_date), ('dob', '<=', rec.to_date)], context=cotext)
            students = student_obj.browse(cr, uid, student_ids, context=context)
            for student in students:
                dob = student.dob
                if dob:
                    age = (datetime.now() - datetime.strptime(dob, '%Y-%m-%d')).days / 365
                    student_obj.write(cr, uid, [student.id], {'age': age}, context=context)
        return True

    # v8 code
    @api.multi
    def calc_age(self):
        student_obj = self.env['student.student']
        for rec in self:
            students = student_obj.search([('dob', '>=', rec.from_date), ('dob', '<=', rec.to_date)])
            for student in students:
                dob = student.dob
                if dob:
                    student.age = (datetime.now() - datetime.strptime(dob, '%Y-%m-%d')).days / 365
        return True