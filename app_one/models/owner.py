from odoo import models, fields


class Owner(models.Model):
    _name = 'owner'


    name = fields.Char(required=1)
    active = fields.Boolean(default=True)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')