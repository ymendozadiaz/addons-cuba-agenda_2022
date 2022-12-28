# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _
from datetime import datetime 
from odoo.exceptions import UserError

class ticket_c(models.Model): 
    _name = 'ticket_c' 
    _inherit = ['mail.thread','mail.activity.mixin','validate.account.move']
      
    name = fields.Char(string='name', required=True, tracking=True) 
    
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True
                            , default=lambda self: _('New'))
    
    price = fields.Integer(string='price', default='100', required=True, tracking=True) 
     
    note = fields.Text(string='note', required=True, tracking=True) 
 
    state = fields.Selection([('new', 'new'), ('validated', 'Validated'), ('finish', 'finish'), ('cancel', 'Cancel')]
                                 , default='new', string="Status", tracking=True)
    
    def action_validated(self):
        self.state = 'validated'
        
    def action_finish(self):
        self.state = 'finish'
    
    def action_new(self):
        self.state = 'new'
        
    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Ticket"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('ticket_c') or _('New')
        res = super(ticket_c, self).create(vals)
        return res

    