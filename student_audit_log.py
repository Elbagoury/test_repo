from openerp import models, fields

class student_audit_log(models.Model):

    _name = 'student.audit.log'

    user_id = fields.Many2one("res.users", "User")
    date = fields.Datetime("Date")
    student_id = fields.Many2one("student.student", "Student")
    status = fields.Selection([('create','Created'),('copy','Copied'),('write','Updated'),('delete','Deleted')], "Status")