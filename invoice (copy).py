import logging
import xmlrpclib
from openerp import models, fields, _
from openerp.addons.connector.queue.job import job, related_action
from openerp.addons.connector.unit.synchronizer import Exporter
from openerp.addons.connector.event import on_record_create
from openerp.addons.connector_ecommerce.event import (on_invoice_paid,
			                                                      on_invoice_validated)
from openerp.addons.connector.exception import IDMissingInBackend
from .unit.backend_adapter import GenericAdapter
from .connector import get_environment
from .backend import magento .....
from .related_action import unwrap_binding
sdsd




_logger = logging.getLogger(__name__)

                                                                                                               sdsd
ds
class MagentoAccountInvoice(models.Model):
    """ Binding Model for the Magento Invoice """
												_name = 'magento.account.invoice'
												_inherit = 'magento.binding'
												_inherits = {'account.invoice': 'openerp_id'}
												_description = 'Magento Invoice'

												openerp_id = fields.Many2one(comodel_name='account.invoice',
																		   string='Invoice',
																		  required=True,
																	    ondelete='cascade')
												magento_order_id = fields.Many2one(comodel_name='ma
