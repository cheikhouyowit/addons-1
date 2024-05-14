# Model de notre Module Keyfa Aboo

from odoo import models, fields, api


class Sale_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    choixbroderie = fields.Many2one('modele.broderie', string="Broderie")
    image_broderie = fields.Binary('Image broderie')
    #choixtissu = fields.Boolean('Avec Tissu')
    choixstyle = fields.Selection(selection=[('sl','Slim'), ('nl', 'Normal'), ('lg', 'Large')], string="Style ")
    choixlongueur = fields.Selection(selection=[('long', 'Long'), ('3quart', '3/4')], string="Longueur")
    choixmanches = fields.Many2one('modele.manche', string="Poignet")



class Keyfaaboo_production_template(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    choixbroderie = fields.Many2one('modele.broderie', string="Broderie", compute='_compute_champs')
    image_broderie = fields.Binary('Image broderie', compute='_compute_champs')
    choixtissu = fields.Boolean('Avec Tissu', compute='_compute_champs')
    choixstyle = fields.Selection(selection=[('sl', 'Slim'), ('nl', 'Normal'), ('lg', 'Large')], string="Style ", compute='_compute_champs')
    choixlongueur = fields.Selection(selection=[('long', 'Long'), ('3quart', '3/4')], string="Longueur", compute='_compute_champs')
    choixmanches = fields.Many2one('modele.manche', string="Poignet", compute='_compute_champs')

    #@api.multi
    def _compute_champs(self):
        def get_parent_move(move):
            if move.move_dest_ids:
                return get_parent_move(move.move_dest_ids)
            return move

        for production in self:
            move = get_parent_move(production.move_finished_ids[0])
            production.choixbroderie = move.sale_line_id and move.sale_line_id and move.sale_line_id.choixbroderie or False
            production.image_broderie = move.sale_line_id and move.sale_line_id and move.sale_line_id.image_broderie or False
            production.choixtissu = move.sale_line_id and move.sale_line_id and move.sale_line_id.choixtissu or False
            production.choixstyle = move.sale_line_id and move.sale_line_id and move.sale_line_id.choixstyle or False
            production.choixlongueur = move.sale_line_id and move.sale_line_id and move.sale_line_id.choixlongueur or False
            production.choixmanches = move.sale_line_id and move.sale_line_id and move.sale_line_id.choixmanches or False

