
from odoo import models, fields, api, exceptions, _
from datetime import datetime
from odoo.tools import format_datetime

class DscAttendance(models.Model):
    _name = "dsc.attendance"
    _description = "DSC Custom Attendance Model"

    # def _default_employee(self):
    #     return self.env.user.employee_id

    name = fields.Char(string='Attendance', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)   
    time_in = fields.Datetime(string="Time In")
    time_out = fields.Datetime(string="Time Out")
    totalworked_hours = fields.Float(string='Total Worked Hours', compute='_compute_totalworked_hours', store=True, readonly=True) #out - in

    regularworked_hours = fields.Float(string='Regular Worked Hours', compute='_compute_regularworked_hours', store=True, readonly=True) # 8 hours
    overtimeworked_hours = fields.Float(string='Overtime Worked Hours', compute='_compute_overtimeworked_hours', store=True, readonly=True) # > 8 hours
    nightdifferential_hours = fields.Float(string='Night Differential Worked Hours', compute='_compute_nightdifferential_hours', store=True, readonly=True) # Additional Settings

    state = fields.Selection([('draft','Draft'),('validated','Validated'),('conflict','Conflict'),('cancelled','Cancelled')], 
            default="draft", tracking=True, string="Status")

    def action_draft(self):
        self.state = 'draft'

    def action_validated(self):
        self.state = 'validated'

    def action_conflict(self):
        self.state = 'conflict'

    def action_cancelled(self):
        self.state = 'cancelled'

    @api.depends('time_in', 'time_out')
    def _compute_totalworked_hours(self):
        for attendance in self:
            if attendance.time_out and attendance.time_in:
                delta = attendance.time_out - attendance.time_in
                attendance.totalworked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.totalworked_hours = False

    @api.depends('time_in', 'time_out')
    def _compute_regularworked_hours(self):
        for attendance in self:
            if attendance.time_out and attendance.time_in:
                delta = attendance.time_out - attendance.time_in
                totalworked_hours = delta.total_seconds() / 3600.0
                if(totalworked_hours > 8):
                    attendance.regularworked_hours = 8
                else:
                    attendance.regularworked_hours = totalworked_hours
            else:
                attendance.totalworked_hours = False

    @api.depends('time_in', 'time_out')
    def _compute_overtimeworked_hours(self):
        for attendance in self:
            if attendance.time_out and attendance.time_in:
                delta = attendance.time_out - attendance.time_in
                totalworked_hours = delta.total_seconds() / 3600.0
                if(totalworked_hours > 8):
                    attendance.overtimeworked_hours = totalworked_hours - 8
                else:
                    attendance.overtimeworked_hours = 0 
            else:
                attendance.overtimeworked_hours = False

    @api.depends('time_in', 'time_out')
    def _compute_nightdifferential_hours(self):
        for attendance in self:
            if attendance.time_out and attendance.time_in:
                nd_starttime =  attendance.time_out.strftime("%m/%d/%Y") + ", 12:00:00" #UTC TIME = 8PM UTC+8
                print("TIMENF ", nd_starttime)

                timeout = attendance.time_out.strftime("%H:%M:%S")
                print("TIMEOUT ", timeout)

                timend = datetime.strptime(nd_starttime, "%m/%d/%Y, %H:%M:%S")
                print("TIMEND ", timend.strftime("%H:%M:%S"))


                delta = attendance.time_out - timend
                totalnd_hours = delta.total_seconds() / 3600.0
                if(totalnd_hours > 0):
                    attendance.nightdifferential_hours = totalnd_hours
                else:
                    attendance.nightdifferential_hours = 0 
            else:
                attendance.nightdifferential_hours = False

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dsc.attendance.seq') or _('New')

        return super(DscAttendance, self).create(vals)