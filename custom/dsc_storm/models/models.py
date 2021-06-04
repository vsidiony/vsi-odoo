# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dsc_storm(models.Model):
    _name = 'dsc.storm'
    _description = 'DSC Storm Model'

    name = fields.Char(string="Storm")
    value = fields.Integer(string="Primary")
    value2 = fields.Float(string="10 %", compute="_value_pc", store=True)
    description = fields.Text("Desc")

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
