from odoo import models, fields

class DscHrEmployeeSettings(models.TransientModel):
    _inherit = "res.config.settings"

    hr_employee_computation_source = fields.Boolean(string="Computation Source")