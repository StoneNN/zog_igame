# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class IntelligentGame(models.Model):
    """
    Game

    """
    _name = "og.igame"
    _description = "Ientelligent Game"
    _parent_store = True
    _order = 'parent_left'

    name = fields.Char('Name', required=True, 
        index=True, copy=False, default='Game')
    date_game = fields.Datetime('Game Date', required=True, 
        index=True, copy=False, default=fields.Datetime.now,
        help="game date")

    game_type = fields.Selection([
        ('bridge','Bridge'),
        ('chess', 'Chess'),
        ('go','Go'),
        ('ddz','Doudizhu'),
    ],default='bridge'    )

    match_type = fields.Selection([
        ('team','Team'),
        ('pair', 'Pair'),
    ],default='team'    )

    org_type = fields.Selection([
        ('items',    'By Items'),  #  go or chess or bridge or ddz
        ('stages',   'By Stages'),
        ('groups',   'By Groups'),
        ('circle',   'Circle'),
        ('swiss',    'Swiss'),
    ],default='swiss'    )

    score_type = fields.Selection([
        ('IMP',   'IMP'),
        ('MP',    'MP'),
    ],default='IMP'    )

    score_uom = fields.Selection([
        ('IMP','IMP'),
        ('MP', 'MP'),
        ('VP', 'VP'),
        ('BAM','BAM'),
    ], compute='_compute_score_uom', inverse='_inverse_score_uom',default='VP' )

    @api.multi
    def _inverse_score_uom(self):
        ds = {'IMP':'IMP','MP': 'MP', 'VP': 'IMP','BAM':'MP'}
        for rec in self:
            rec.score_type = ds[rec.score_uom]

    @api.multi
    def _compute_score_uom(self):
        fns = {
            'team': lambda t: {'IMP': 'VP','MP':'BAM'}[t],
            'pair': lambda t: t
        }

        for record in self:
            record.score_uom = fns[record.match_type](record.score_type)


    state = fields.Selection([
        ('draft',      'Draft'),
        ('conformed',  'Regitering'),
        ('locked',     'Locked'),
        ('ready',      'Doing'),
        ('done',       'Done'),
        ('cancel',     'Cancelled')

        ], string='Status', readonly=True, 
        index=True, copy=False, default='draft')

    @api.multi
    def action_confirmed(self):
        return self.write({'state': 'confirmed'})

    @api.multi
    def action_locked(self):
        return self.write({'state': 'locked'})

    @api.multi
    def action_ready(self):
        return self.write({'state': 'ready'})

    @api.multi
    def action_done(self):
        return self.write({'state': 'done'})

    @api.multi
    def action_cancel(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def action_draft(self):
        return self.write({'state': 'draft'})




    notes = fields.Text('Notes')

    parent_id = fields.Many2one('og.igame', string='Parent Game', index=True, ondelete='restrict')
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)

    sequence = fields.Integer(default=10,
        help="Sequence of Children")

    child_ids = fields.One2many('og.igame', 'parent_id', string='Child Game')

    partner_ids = fields.Many2many('res.partner', string='Teams',
        compute='_compute_partner')

    # Only for Team Match
    group_ids = fields.One2many('og.igame.group','igame_id',string='Groups')
    round_ids = fields.One2many('og.igame.round','igame_id',string='Rounds')
    # Only for Team Match

    score_ids = fields.One2many('og.igame.score', 'igame_id', string='Teams Score')
    deal_ids = fields.Many2many('og.deal',string='Deals')

    # for Pair Match
    table_ids = fields.Many2many('og.table')

    @api.multi
    def _compute_partner(self):
        for record in self:
            record.partner_ids = record.score_ids.mapped('partner_id')


class IntelligentGameGroup(models.Model):
    """
    # Only for Team Match
    """

    _name = "og.igame.group"
    _description = "iGame Group"
    _order = 'sequence, name'

    name = fields.Char('Name')
    sequence = fields.Integer()
    igame_id = fields.Many2one('og.igame','Game')
    partner_ids = fields.Many2many('res.partner')

class IntelligentGameRound(models.Model):
    """
    # Only for Team Match
    """

    _name = "og.igame.round"
    _description = "iGame Round"
    _rec_name = 'number'
    _order = 'number'

    igame_id = fields.Many2one('og.igame','Game')
    name = fields.Char('Name',related='igame_id.name')
    number = fields.Integer('Number')
    round  = fields.Integer('Number', related='number')

    deal_ids = fields.Many2many('og.deal',string='Deals')

    #  for  game room
    score_line_ids = fields.One2many('og.igame.score.line','round_id')
    table_ids = fields.Many2many('og.table', compute='_compute_table')

    @api.multi
    def _compute_table(self):
        for rec in self:
            matchs = rec.score_line_ids.mapped('match_id')
            open  = matchs.mapped('open_table_id')
            close = matchs.mapped('close_table_id')
            rec.table_ids = open | close
