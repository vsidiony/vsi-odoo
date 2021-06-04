
from odoo import models, fields, api, _
from datetime import datetime

class DscStormLog(models.Model):
    _name = "dsc.storm.log"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Storm Log Model"

    name = fields.Char(string='Storm', required=True)
    storm_code = fields.Char(string='Code', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    description = fields.Text(string='Description')
    storm_type = fields.Selection([
        ('blizzard', 'Blizzard'),
        ('dust_storm', 'Dust Storm'),
        ('hail_storm', 'Hail Storm'),
        ('snow_storm', 'Snow Storm'),
        ('wind_storm', 'Wind Storm'),
        ('other', 'Other'),
    ], required=True, default='wind_storm', tracking=True, help="Type of storm")
    location = fields.Text(string='Location')
    start_date = fields.Date(string="Start Date", default=datetime.today())
    state = fields.Selection([('build','Build Up'),('ongoing','Ongoing'),('done','Done')], 
    default="build", tracking=True, string="Status")
    manager_id = fields.Many2one('res.partner', string="Manager")

    def action_ongoing(self):
        self.state = 'ongoing'

    def action_done(self):
        self.state = 'done'

    @api.model
    def create(self, vals):
        if not vals.get('location'):
            vals['location'] = 'Philippines'
       
        if vals.get('storm_code', _('New')) == _('New'):
            vals['storm_code'] = self.env['ir.sequence'].next_by_code('dscstorm.log') or _('New')

        return super(DscStormLog, self).create(vals)