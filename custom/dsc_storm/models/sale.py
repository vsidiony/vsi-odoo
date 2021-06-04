
from odoo import models, fields

class DscStormLog(models.Model):
    _inherit = "sale.order"

    storm_sale_description = fields.Char(string="Storm Sales")