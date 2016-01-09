import time
from datetime import datetime
from openerp.exceptions import Warning
from openerp import models, fields,api, _

class student_student(models.Model):

    _name = 'student.student'

    _description = 'Student'

    #You can create table with specific name otherwise it will create table with model name and replace . with _
    # _table = 'student_student_info'

    _order = 'student_number'

    def _get_student_number(self):
        return self.env['ir.sequence'].get('student.student')

    student_number = fields.Char('Student Number', required=True, copy=False)
    name = fields.Char('Name', copy=False)
    age = fields.Integer('Age')
    dob = fields.Date('Date of Birth')
    test_float = fields.Float('Fees')
    address_id = fields.Many2one("res.partner", "Address Info.", copy=False)
    email = fields.Char(related= "address_id.email",string="Email")
    # contact = fields.Char(related="address_id.mobile", string="Contact")
    #To check constraint we have removed related from contact field
    contact = fields.Char("Contact")
    address = fields.Text('Address')
    image = fields.Binary('Image')
    accepted = fields.Boolean('Is Accepted?', default=True)
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], 'Gender', default = 'm')
    reference_ids = fields.One2many('reference.reference', 'student_id', string="References")
    hobbies_ids = fields.Many2many('hobbie.hobbie', "student_hobbie_rel", 'student_id', 'hobby_id', string="Hobbies")
    course_id = fields.Many2one('course.course', "Course")
    state = fields.Selection([('draft','New'), ('confirm','Confirmed'), ('register','Registered'), ('cancel','Cancel'), ('reject', 'Reject'), ('done', 'Done')], "State", default='draft')
    type = fields.Selection([('student','Student'),('faculty','Faculty')], "Type")
    note = fields.Text('Internal Note')

    _sql_constraints = [('unique_stud_number', 'unique(student_number)', 'Student Number should be unique.'),]

    @api.one
    @api.constrains('contact',)
    def _check_contact(self):

        if self.contact:
            if not (self.contact).isdigit() or len(self.contact)!=10:
                raise Warning(_('User Error'),_("Entered Number is in wrong format, You are only allowed to enter number"))
        print "Constraint method is being called..."


    @api.onchange('course_id',)
    def _get_course_fees(self):

        if self.course_id:
            self.test_float = self.course_id.fees

    @api.model
    def default_get(self, fields):

        print "Fields Info::",fields
        res = super(student_student, self).default_get(fields)
        next_seq_number  = self.env['ir.sequence'].get('student.student')
        print "next_seq_number :::",next_seq_number
        print "RESult :::",res
        res.update({'student_number':next_seq_number})
        return res

    @api.multi
    def action_calc_age(self):
        # your code goes here
        print "\n\n#########action_calc_age#################"
        # gives the database ID of passed xml ID
        # param1: module name, param2: xml ID
        # returns (view_name, database ID): Ex:(u'ir.ui.view', 211)
        res_view_id = self.env['ir.model.data'].get_object_reference('training_8', 'view_wiz_calc_age_form')[1]
#        res_view_id = self.env['ir.model.data'].get_object_reference('training_8', 'view_wiz_calc_age_form2')[1]
        return {
            'name': "Calculate Age (Object)",
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': res_view_id,
            'res_model': 'wiz.calc.age',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_to_date': time.strftime('%Y-%m-%d')} # default_your_field_name
        }

    @api.model
    def create(self, vals):
        res = super(student_student, self).create(vals)
        audit_log_data = {'user_id':self._uid,
                          'date':datetime.now(),
                          'student_id':res.id,
                          'status':'create'
                          }
        self.env['student.audit.log'].create(audit_log_data)
        return res

    @api.one
    def copy(self):

        res = super(student_student, self).copy()
        audit_log_data = {'user_id':self._uid,
                          'date':datetime.now(),
                          'student_id':res.id,
                          'status':'copy'
                          }
        self.env['student.audit.log'].create(audit_log_data)
        return res

    @api.multi
    def write(self, vals):
        """
        :param vals: updated columns dictionary
        :return: This method will return true or False and creates the entries in audit log table.
        """

        for student in self:
            audit_log_data = {'user_id':self._uid,
                          'date':datetime.now(),
                          'student_id':student.id,
                          'status':'write'
                          }
            self.env['student.audit.log'].create(audit_log_data)
        res = super(student_student, self).write(vals)
        return res

    @api.multi
    def unlink(self):
        """
        :return: Restricted user to unlink records if confirmed or registered and return True or False
        IF record will unlink it creates entries in audit log table
        """

        #This loop will check for all records those are selected for deletion if wrong selected it will raise warning
        for student in self:
            if student.state not in ['draft','cancel']:
                raise Warning(_('User Error'), _("You are not allow to delete the selected records"))

        for student in self:
            audit_log_data = {'user_id':student._uid,
                          'date':datetime.now(),
                          'student_id':student.id,
                          'status':'delete'
                          }
            self.env['student.audit.log'].create(audit_log_data)
        res = super(student_student, self).unlink()
        print "res :::::::::::::",res
        return res

    @api.multi
    def register(self):
        """
        :return: This will update the current state from new to register
        """
        for student in self:
            student.state = 'register'

    @api.multi
    def confirm(self):
        """
        :return: This will update the current state from new to register
        """
        for student in self:
            student.state = 'confirm'

    @api.multi
    def cancel(self):
        """
        :return: This will update the current state from new to register
        """
        for student in self:
            student.state = 'cancel'

    @api.multi
    def reject(self):
        return {
            'name': "Reject Reason",
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'wiz.reject.reason',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirm'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_register(self):
        self.write({'state': 'register'})

    @api.multi
    def action_reject(self):
        self.write({'state': 'reject'})

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

class reference_reference(models.Model):

    _name = 'reference.reference'

    student_id = fields.Many2one("student.student", "Student")
    name = fields.Char("Name")
    contact = fields.Char("Contact")
    email = fields.Char("Email")


class hobbie_hobbie(models.Model):

    _name = 'hobbie.hobbie'

    name = fields.Char("Hobby")


class course_course(models.Model):

    _name = 'course.course'

    _description = "Course"

    _rec_name = 'code'

    name = fields.Char("Name")
    code = fields.Char("Code")
    fees = fields.Char("Course Fees")


    @api.multi
    def name_get(self):
        """
        :return: Override the name_get method to get the combination of name and code as display value
        when adding course for student.
        """


        res = super(course_course, self).name_get()
        new_result = []
        for course in self:
            new_info = ""
            new_info += course.name or ""
            new_info += " ["
            new_info += course.code
            new_info += "]"
            new_result.append((course.id, new_info))

        return new_result

