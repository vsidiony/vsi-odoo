from odoo import models, fields

class DscHrEmployeeSettings(models.TransientModel):
    _inherit = "res.config.settings"

    hr_employee_computation_source = fields.Boolean(string="Computation Source")
    night_differential_start_time = fields.Char(string="Night Differential Start Time")
    night_differential_end_time = fields.Char(string="Night Differential End Time")

    def set_values(self):
        super(DscHrEmployeeSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('dsc_attendance.hr_employee_computation_source', self.hr_employee_computation_source)

        ndstvals = self.night_differential_start_time.split(':')
        t, ndsthours = divmod(float(ndstvals[0]), 24)
        t, ndstminutes = divmod(float(ndstvals[1]), 60)
        ndstminutes = ndstminutes / 60.0

        ndetvals = self.night_differential_end_time.split(':')
        t, ndethours = divmod(float(ndetvals[0]), 24)
        t, ndetminutes = divmod(float(ndetvals[1]), 60)
        ndetminutes = ndetminutes / 60.0

        self.env['ir.config_parameter'].sudo().set_param('dsc_attendance.night_differential_start_time', ndsthours + ndstminutes)
        self.env['ir.config_parameter'].sudo().set_param('dsc_attendance.night_differential_end_time', ndethours + ndetminutes)

    def get_values(self):
        res = super(DscHrEmployeeSettings, self).get_values()

        hr_employee_computation_source = self.env['ir.config_parameter'].get_param('dsc_attendance.hr_employee_computation_source')        
        res.update({'hr_employee_computation_source': hr_employee_computation_source})

        night_differential_start_time = self.env['ir.config_parameter'].get_param('dsc_attendance.night_differential_start_time')
        ndsthour, ndstminute = divmod(float(night_differential_start_time), 1)
        ndstminute *= 60
        dnst = '{}:{}'.format(int(ndsthour), int(ndstminute))
        res.update({'night_differential_start_time': dnst})

        night_differential_end_time = self.env['ir.config_parameter'].get_param('dsc_attendance.night_differential_end_time')
        ndethour, ndetminute = divmod(float(night_differential_end_time), 1)
        ndetminute *= 60
        dnet = '{}:{}'.format(int(ndethour), int(ndetminute))
        res.update({'night_differential_end_time': dnet})

        return res