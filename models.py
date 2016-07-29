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
		self.delivered = 0

	delivered = fields.Integer(string='Entregados',compute=_compute_delivered_qty)
