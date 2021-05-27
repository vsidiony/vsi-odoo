# -*- coding: utf-8 -*-
from odoo import http


class DscStorm(http.Controller):
    @http.route('/dsc_storm/dsc_storm/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/dsc_storm/dsc_storm/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('dsc_storm.listing', {
            'root': '/dsc_storm/dsc_storm',
            'objects': http.request.env['dsc.storm'].search([]),
        })

    @http.route('/dsc_storm/dsc_storm/objects/<model("dsc.storm"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('dsc_storm.object', {
            'object': obj
        })
