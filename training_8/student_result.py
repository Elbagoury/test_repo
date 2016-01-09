from openerp import models, fields,api, _


class student_result(models.Model):
    
        _name = 'student.result'
        
        name=fields.Char("Name")
        
        course_id=fields.Many2one('course.course','Course id')
        date=fields.Date("Date")
        marks_lines=fields.One2many('student.result.line',"Result Line")





class student_result_line(models.Model):

    _name='student.result.line'
    
    subject_id=fields.Many2one("subject.subject","Subject")
    total_mark=fields.Char("Total Mark")
    