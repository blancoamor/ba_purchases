from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate
from datetime import datetime

#Get the logger
_logger = logging.getLogger(__name__)


class purchase_order(models.Model):
	_inherit = 'purchase.order'

	@api.one
	def _compute_match_delivered(self):
		return_value = True
		for line in self.order_line:
			if line.product_qty != line.delivered:
				return_value = False
		self.match_delivered = return_value

	@api.one
	def _compute_match_invoiced(self):
		return_value = True
		for line in self.order_line:
			if line.product_qty != line.invoiced:
				return_value = False
		self.match_invoiced = return_value

	match_delivered = fields.Boolean('Coinciden Entregas',compute=_compute_match_delivered)
	match_invoiced = fields.Boolean('Coinciden Facturas',compute=_compute_match_invoiced)

class purchase_order_line(models.Model):
	_inherit = 'purchase.order.line'

	@api.one
	def _compute_delivered_qty(self):
		return_value = 0
		if self.move_ids:
			for stock_move in self.move_ids:
				if stock_move.state == 'done':
					return_value = return_value + stock_move.product_qty
		self.delivered = return_value

	@api.one
	def _compute_invoiced_qty(self):
		return_value = 0
		if self.invoice_lines:
			for invoice_line in self.invoice_lines:
				if invoice_line.invoice_id.state in ['open','paid']:
					return_value = return_value + invoice_line.quantity
		self.invoiced = return_value		

	@api.one
	def _compute_invoiced_amount(self):
		return_value = 0
		if self.invoice_lines:
			for invoice_line in self.invoice_lines:
				if invoice_line.invoice_id.state in ['open','paid']:
					return_value = return_value + invoice_line.quantity * invoice_line.price_unit
		self.invoiced_amount = return_value

	delivered = fields.Integer(string='Entregados',compute=_compute_delivered_qty)
	invoiced = fields.Integer(string='Facturados',compute=_compute_invoiced_qty)
	amount_invoiced = fields.Float(string='Monto facturado',compute=_compute_invoiced_amount)
