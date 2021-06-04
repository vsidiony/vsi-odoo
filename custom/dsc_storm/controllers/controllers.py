# -*- coding: utf-8 -*-
from odoo import http
import json
import pymssql
import asana

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

    @http.route('/dsc_storm/test_mssql/', auth='public')
    def test_mssql(self, **kw):    
        sqlserver = "SQL5074.site4now.net";
        sqluser = "DB_A62889_dncoredemodb_admin"
        sqlpassword = "890IOPjkl"
        sqldatabase = "DB_A62889_dncoredemodb"
        con = pymssql.connect(sqlserver, sqluser, sqlpassword, sqldatabase)

        sqlquery = "SELECT * FROM AspNetUsers";

        cursor = con.cursor(as_dict=True)
        cursor.execute(sqlquery);
        result = "{"
        for row in cursor:
            print("UserName=%s" % (row['UserName']))    
            result += "{ \"UserName\":" + row['UserName'] + "}"
            
        result += "}"

        return json.dumps(result)

    @http.route('/dsc_storm/test_asana/', auth='public')
    def test_asana(self, **kw):    
        asanaapi = "https://app.asana.com/api/";
        version = "1.0"
        endpoint = "users/me"
        pat = "1/1200399901857850:6c3f296fcb07972a86e45f20978737b3"

        client = asana.Client.access_token(pat)

        me = client.users.me()

        print(me)
         
        return json.dumps(me)

    @http.route('/dsc_storm/test_asana_projects/', auth='public')
    def test_asana_projects(self, **kw):    
        asanaapi = "https://app.asana.com/api/";
        version = "1.0"
        endpoint = "users/me"
        pat = "1/1200399901857850:6c3f296fcb07972a86e45f20978737b3"

        client = asana.Client.access_token(pat)

        projects = client.projects.get_projects()

        print(projects)
         
        return json.dumps(projects)