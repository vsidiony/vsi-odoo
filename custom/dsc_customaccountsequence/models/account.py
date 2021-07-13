from odoo import models, fields, api, _


class DscAccountMove(models.Model):
    _inherit = "account.move"

    vsi_custom_sequence = fields.Char(string="VSI Sequence", required=True, copy=False, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):

        if vals.get('vsi_custom_sequence', _('New')) == _('New'):
            vals['vsi_custom_sequence'] = self.env['ir.sequence'].next_by_code('vsi.customer.invoice') or _('New')

        return super(DscAccountMove, self).create(vals)