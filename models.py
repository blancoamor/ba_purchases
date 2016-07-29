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

	delivered = fields.Integer(string='Entregados',compute=_compute_delivered_qty)
