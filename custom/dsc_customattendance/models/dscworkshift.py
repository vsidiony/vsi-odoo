
from odoo import models, fields, api, exceptions, _
from datetime import datetime
from odoo.tools import format_datetime

class DscWorkShiftSchedule(models.Model):
    _name = "dsc.work.shift.schedule"
    _description = "DSC Custom Work Shift Schedule Model"

    name = fields.Char(string='Shift', required=True)
    time_in = fields.Char(string="Time In [HH:mm]")
    time_out = fields.Char(string="Time Out [HH:mm]")
    totalwork_hours = fields.Float(string='Total Work Hours', compute='_compute_totalwork_hours', store=True, readonly=True) #out - in
    minimum_overtime_minutes = fields.Float(string='Minimum Overtime Minutes') # 8 hours
    nightdifferential_start_time = fields.Float(string='Night Differential Start Time [HH:mm]') # > 8 hours

    @api.depends('time_in', 'time_out')
    def _compute_totalwork_hours(self):
        for attendance in self:
            if attendance.time_out and attendance.time_in:
                delta = attendance.time_out - attendance.time_in
                attendance.totalwork_hours = delta.total_seconds() / 3600.0
            else:
                attendance.totalwork_hours = False
