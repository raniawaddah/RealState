from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=1, default='name', size=10)
    ref = fields.Char(default='New', readonly=1)
    active = fields.Boolean(default=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff',)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='south')

    owner_id = fields.Many2one('owner', )
    tag_ids = fields.Many2many('tag', )
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),

    ], default='draft', )


    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!!')
    ]

    line_ids = fields.One2many('property.line', 'property_id')

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print("inside _onchange_expected_price method ")
            return {
                'warning': {'title': "Warning", 'message': "Negative Value", 'type': 'notification'},
            }


    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            print("inside _compute_diff method ")
            rec.diff = rec.expected_price - rec.selling_price

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms!')


    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True


    def action(self):
        print(self.env['owner'].create({
            'name': 'name one',
            'phone': '010000000'
        }))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_Seq')
        return res



    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     print("inside create method")
    #     return res
    #
    # @api.model
    #
    # def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    #
    #     res = super(Property, self)._search(args, offset=0, limit=None, order=None, count=False, access_rights_uid=None)
    #     print("inside search method")
    #     return res
    #
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("inside write method")
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink method")
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()