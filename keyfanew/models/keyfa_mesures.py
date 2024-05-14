from odoo import api,models,fields


class keyfa_mesure(models.Model):
    _name = 'order.mesure'



    sale = fields.Many2one('sale.order', string='Bon de commande')
    sale_line = fields.Many2one('sale.order.line', string='Ligne Bon de commande')
    mrp = fields.Many2one('mrp.production', string='Bon de production')

    name = fields.Many2one('res.partner', string='Client')
    sexe = fields.Selection(selection=[('h', 'Homme'), ('f', 'Femme')] , string="Mesure pour : ")
    L_Epaul = fields.Integer("L_Epaul")
    T_Cou = fields.Integer("T_Cou")
    C_Bat = fields.Integer("C_bat")
    V_Pince = fields.Integer("V_Pince")
    AT_Poitr = fields.Integer("AT_Poitr")
    T_Poitr = fields.Integer("T_Poitr")
    T_Taille = fields.Integer("T_Taille")
    Ceint = fields.Integer("Ceint")
    T_Bn = fields.Integer("T_Bn")
    T_Hanc = fields.Integer("T_Hanc")
    L_Manc = fields.Integer("L_Manc")
    L_Manch3_4 = fields.Integer("L_Manch3_4")
    T_Bras = fields.Integer("T_Bras")
    T_Poignet = fields.Integer("T_Poignet")
    T_Cuisse = fields.Integer("T_Cuisse")
    L_Genoux = fields.Integer("L_Genoux")
    L_3_4 = fields.Integer("L_3/4")
    M_courte = fields.Integer("M_courte")
    L_Haut = fields.Integer("L_Haut")
    L_Jupe = fields.Integer("L_Jupe")
    LJ_crt = fields.Integer("LJ_crt")
    L_Bas = fields.Integer("L_Bas")
    L_Pant = fields.Integer("L_Pant")
    L_T = fields.Integer("LT")
    Carrure_dos = fields.Integer("Carrure_dos")
    Carrure_devant = fields.Integer("Carrure_devant")
    Longueur_dos = fields.Integer("Longueur_dos")
    T_Chem = fields.Integer("taille Chemise")
    T_Pant = fields.Integer("taille Pantalon")
    T_Veste = fields.Integer("taille Veste")
    T_Stat = fields.Integer("taille Stature")
    #Style = fields.selection(('slim','SLIM'),('normal','NORMAL'),('large','LARGE'))
    Gabarit = fields.Boolean('Gabarit')
    Broderie   = fields.Selection((('ton_sur_ton','TON SUR TON'),('leg_ton_ton','LEGEREMENT TON SUR TON'),
                              ('flashy','FLASHY')))


class modele_broderie(models.Model):
    _name = 'modele.broderie'

    name = fields.Char(string="Reference broderie")
    image = fields.Binary('Image', filters='*.png,*.gif')


class modele_tissu(models.Model):
    _name = 'modele.tissu'

    name = fields.Char(string="Reference Tissu")
    image = fields.Binary('Image', filters='*.png,*.gif')

class modele_manches(models.Model):
    _name = 'modele.manche'

    name = fields.Char(string="Type de manches")
    image = fields.Binary('Image', filters='*.png,*.gif')



class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    partner_mesure = fields.One2many('order.mesure','name' , string='Mesures', limit = 1)
    s_couvert = fields.Char('sous couvert de:')

class Sale_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    mesure_test = fields.Boolean('Mesure du client?')
    mesures = fields.Many2one('order.mesure', string='Mesures')
    choixtissu = fields.Boolean('Avec Tissu')
    choixmesure = fields.Boolean('Mesure Client?')

    @api.onchange('choixtissu')
    def onchange_with_cloth(self):
        if self.choixtissu:
            self.price_unit = self.product_id.lst_price - 20000
        else:
            self.price_unit = self.product_id.lst_price

    @api.onchange('choixmesure')
    def onchange_with_mesure(self):
        if self.choixmesure:
           self.mesures = self.order_partner_id.partner_mesure
        else:
            self.mesures = None

    @api.onchange('choixbroderie')
    def onchange_broderie(self):
        if self.choixbroderie:
            self.image_broderie = self.choixbroderie.image



class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    sale_mesures = fields.Many2one('order.mesure' , compute='_compute_sale_mesures', string='Mesures client')

    #@api.multi
    def _compute_sale_mesures(self):
     def get_parent_move(move):
        if move.move_dest_ids:
            return get_parent_move(move.move_dest_ids)
        return move

     for production in self:
         move = get_parent_move(production.move_finished_ids[0])
         production.sale_mesures = move.sale_line_id and move.sale_line_id and move.sale_line_id.mesures or False


class ProductProduct(models.Model):
    _inherit = 'product.product'

    route_ids = fields.Many2many('stock.location.route', 'stock_route_variant',
        'product_id', 'route_id',
        'Routes', domain="[('product_selectable', '=', True)]",
        help="Depending on the modules installed, this will allow you to define the route of the product: whether it will be bought, manufactured, MTO/MTS,...")
