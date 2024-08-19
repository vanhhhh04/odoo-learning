# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
class BassArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Abstract Archive'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active



class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    _order = 'date_release desc, name'
    
    name = fields.Char('Title', required=True, index=True)
    short_name = fields.Char('Short Title',translate=True, index=True)
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State', default="draft")
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated', copy=False)
    pages = fields.Integer('Number of Pages',
        groups='base.group_user',
        states={'lost': [('readonly', True)]},
        help='Total book page count', company_dependent=False)
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4),  # Optional precision (total, decimals),
    )
    author_ids = fields.Many2many('res.partner', string='Authors')
    cost_price = fields.Float('Book Cost', digits='Book Price')
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price') # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    category_id = fields.Many2one('library.book.category')
    age_days = fields.Float(string='Days Since Release',compute='_compute_age',inverse='_inverse_age',search='_search_age',store=False)

    publisher_city = fields.Char('Publisher City',related='publisher_id.city',readonly=True)
    # _sql_constraints = [('name_uniq', 'UNIQUE(name)','Book title must be unique.'),('positive_page', 'CHECK(pages>0)','No of pages must be positive')]
    # _sql_constraints = [('check_cost_price', 'CHECK(cost_price>0)', 'the cost_price have to be positive')]
    
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state,new_state):
                book.state = new_state
            else:
                mgs = f'Moving from {book.state} to {new_state} is not allowed'
                raise UserError(mgs) 
    
    def make_available(self):
        self.change_state('available')
    
    def make_borrowed(self):
        self.change_state('borrowed')
    
    def make_lost(self):
        self.change_state('lost')


    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
    ('available', 'borrowed'),
    ('borrowed', 'available'),
    ('available', 'lost'),
    ('borrowed', 'lost'),
    ('lost', 'available')]
        return (old_state, new_state) in allowed

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
        ('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]
    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0
    
    
    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                    raise models.ValidationError('Release date must be in the past')
    
    def name_get(self):
        """ This method used to customize display name of the record """
        result = []
        for record in self:
            rec_name = f"{record.name} ,{record.date_release})"
            result.append((record.id, rec_name))
        return result

class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
    'library.book', 'publisher_id',
    string='Published Books')
    authored_book_ids = fields.Many2many('library.book', string='Authored Books')
    count_books = fields.Integer( 'Number of Authored Books',compute='_compute_count_books')
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)

class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Library Member'

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')