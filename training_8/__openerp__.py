{
    'name': 'Training v8',
    'version': '1.0',
    'author': 'SerpentCS',
    'website': 'www.serpentcs.com',
    'category': 'sale',
    'description': '''
Training of v8.
''',
    'depends': ['sale'],
    'data': [
        'security/security_view.xml',
        'security/ir.model.access.csv',     
        'data/student.student.csv',
        'student_workflow.xml',
        'student_sequence.xml',
        'wizard/wiz_calc_age_view.xml',
        'training_view.xml',
        'student_audit_log_view.xml',
        'res_partner_view.xml',
        'sale_view.xml',
        'wizard/wiz_reject_reason_view.xml',
    ],
    'installable': True,
    'auto-install': False,
    'application':True
}