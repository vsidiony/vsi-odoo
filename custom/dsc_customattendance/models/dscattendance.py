
from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
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

    def action_copy_from_attendance2(self):
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

    @api.model
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

                #hremployee = self.env['hr.employee'].search(['id',"=", self.employee_id])
                #print("RESOURCE CALENDAR ID " + hremployee.resource_calendar_id)

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
                timezone_timeoffset = timedelta(hours=8)

                timezone_adjusted_timein = attendance.time_in + timezone_timeoffset
                timezone_adjusted_timeout = attendance.time_out + timezone_timeoffset
                print("TZ TIMEIN ", timezone_adjusted_timein)
                print("TZ TIMEOUT ", timezone_adjusted_timeout)

                #settings_night_differential_starttime = self.env['ir.config_parameter'].get_param('dsc_attendance.night_differential_start_time')
                night_differential_start_time = self.env['ir.config_parameter'].get_param('dsc_attendance.night_differential_start_time')
                ndsthour, ndstminute = divmod(float(night_differential_start_time), 1)
                ndstminute *= 60
                settings_night_differential_starttime = '{}:{}'.format(int(ndsthour), int(ndstminute))
                
                #settings_night_differential_endtime = self.env['ir.config_parameter'].get_param('dsc_attendance.night_differential_end_time')
                night_differential_end_time = self.env['ir.config_parameter'].get_param('dsc_attendance.night_differential_end_time')
                ndethour, ndetminute = divmod(float(night_differential_end_time), 1)
                ndetminute *= 60
                settings_night_differential_endtime = '{}:{}'.format(int(ndethour), int(ndetminute))

                night_differential_starttime =  timezone_adjusted_timein.strftime("%m/%d/%Y") + ", "+ settings_night_differential_starttime +":00" #UTC TIME = 8PM UTC+8
                dt_night_differential_starttime = datetime.strptime(night_differential_starttime, "%m/%d/%Y, %H:%M:%S")
                print("ND_STARTTIME ", dt_night_differential_starttime)

                timezone_adjusted_timein_nextdate = timezone_adjusted_timein + timedelta(days=1)
                night_differential_endtime = timezone_adjusted_timein_nextdate.strftime("%m/%d/%Y") + ", "+ settings_night_differential_endtime +":00" #UTC TIME = 8PM UTC+8
                dt_night_differential_endtime = datetime.strptime(night_differential_endtime, "%m/%d/%Y, %H:%M:%S")
                print("ND_ENDTIME ", dt_night_differential_endtime)
               
                # ATTENDANCE TIMEOUT : 2021/07/20 19:00:00
                # TIME ND : 2021/07/20 20:00:00      
                if(timezone_adjusted_timeout > dt_night_differential_starttime and timezone_adjusted_timeout <= dt_night_differential_endtime):
                    delta = timezone_adjusted_timeout - dt_night_differential_starttime
                    totalnd_hours = delta.total_seconds() / 3600.0
                    attendance.nightdifferential_hours = totalnd_hours
                elif(timezone_adjusted_timeout > dt_night_differential_starttime and timezone_adjusted_timeout >= dt_night_differential_endtime):
                    delta = dt_night_differential_endtime - dt_night_differential_starttime
                    totalnd_hours = delta.total_seconds() / 3600.0
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