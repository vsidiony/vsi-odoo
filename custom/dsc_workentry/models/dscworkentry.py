
from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from odoo.tools import format_datetime

class DscWorkEntry(models.Model):
    _name = "dsc.work.entry"
    _description = "DSC Custom Work Entry Model"

    name = fields.Char(string='WorkEntry', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)   
    time_in = fields.Datetime(string="Time In")
    time_out = fields.Datetime(string="Time Out")
    totalworked_hours = fields.Float(string='Total Worked Hours') #out - in

    regularworked_hours = fields.Float(string='Regular Worked Hours') # 8 hours
    overtimeworked_hours = fields.Float(string='Overtime Worked Hours') # > 8 hours
    nightdifferential_hours = fields.Float(string='Night Differential Worked Hours') # Additional Settings

    state = fields.Selection([('draft','Draft'),('validated','Validated'),('conflict','Conflict'),('cancelled','Cancelled')], 
            default="draft", tracking=True, string="Status")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dsc.workentry.seq') or _('New')

        return super(DscWorkEntry, self).create(vals)

    
    def action_copy_from_attendance(self):
        hrattendance = self.env['hr.attendance'].search([])

        for attendance in hrattendance:
            print("CHECKIN", attendance.check_in)
            print("CHECKOUT", attendance.check_out)

        timeinstring =  datetime.now().strftime("%m/%d/%Y") + ", 04:00:00"
        timein = datetime.strptime(timeinstring, "%m/%d/%Y, %H:%M:%S")
        self.time_in = timein

        timeoutstring =  datetime.now().strftime("%m/%d/%Y") + ", 23:00:00"
        timeout = datetime.strptime(timeoutstring, "%m/%d/%Y, %H:%M:%S")
        self.time_out = timeout