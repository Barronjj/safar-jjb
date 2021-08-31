import time
import logging
import json
import binascii
import base64
from requests import request
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(selection_add=[("gls_fr", "GLS France"), ("Heppner", "HEPPNER"), ("Kuehne", "KUEHNE et NAGEL")])
    gls_france_service = fields.Selection([('flexDeliveryService', 'Flex Delivery Service')],
                                          string="GLS France Service")

    def gls_fr_rate_shipment(self, order):
        self.ensure_one()
        return {'success': True, 'price': 0.0,'error_message': False, 'warning_message': False}


    def deside_gls_url(self, api_operation):
        if self.company_id and self.company_id.gls_api_url:
            url = self.company_id.gls_api_url + api_operation
            return url
        else:
            raise ValidationError(_("Set the appropriate URL in shipping instance."))

    def gls_api_calling_function(self, api_url, request_data):
        gls_username = self.company_id and self.company_id.gls_username
        gls_password = self.company_id and self.company_id.gls_password
        data = "%s:%s" % (gls_username, gls_password)
        encode_data = base64.b64encode(data.encode("utf-8"))
        authrization_data = "Basic %s" % (encode_data.decode("utf-8"))
        headers = {'Accept-Language':'en',
                   'Accept-Encoding':'gzip,deflate',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': authrization_data}
        data = json.dumps(request_data)
        try:
            _logger.info("GLS URL : %s \n GLS Request Data : %s" % (api_url, data))
            response_body = request(method='POST', url=api_url, data=data, headers=headers)
        except Exception as e:
            raise ValidationError(e)
        return response_body

    def gls_packages_info(self, total_weight=False, packages=False):
        gls_packages = []
        if packages:
            for package in packages:
                parcel_dict = {"weight":"%s"%(package.shipping_weight),"references": ["%s"%(package.name)],"comment": "%s"%(package.name)}
                gls_packages.append(parcel_dict)
                if self.gls_france_service:
                    parcel_dict['services'] = [{"name": "flexDeliveryService"}]
        if total_weight:
            parcel_dict = {"weight":  "{}".format(total_weight), "references": ["BulkPackage"], "comment": ""}
            gls_packages.append(parcel_dict)
            if self.gls_france_service:
                parcel_dict['services'] = [{"name": "flexDeliveryService"}]
        return gls_packages

    def gls_order_request_data(self, picking):
        receipient_address = picking.partner_id
        picking_company_id = picking.picking_type_id.warehouse_id.partner_id
        package_details = picking.package_ids
        total_bulk_weight = picking.weight_bulk
        order_data = {"shipperId": "%s %s"%(self.company_id and self.company_id.gls_customer_id,self.company_id and self.company_id.gls_contact_id),
                      "shipmentDate": "%s"%(time.strftime('%Y-%m-%d')),
                      "references": ["%s"%(picking.name)],
                      "addresses": {
                        "delivery": {
                          "name1":  "%s" % (receipient_address.name),
                          "name2": "",
                          "name3": "",
                          "street1": "%s" % (receipient_address.street or ""),
                          "country": "%s" % (receipient_address.country_id and receipient_address.country_id.code or ""),
                          "zipCode": "%s" % (receipient_address.zip or ""),
                          "city": "%s" % (receipient_address.city or ""),
                          "contact": "",
                          "email": "%s" % (receipient_address.email or ""),
                          "phone": "%s" % (receipient_address.phone or ""),
                          "mobile": ""},
                        "alternativeShipper": {
                          "name1":"%s" % (picking_company_id.name),
                          "name2": "",
                          "name3": "",
                          "street1": "%s" % (picking_company_id.street or ""),
                          "country": "%s" % (picking_company_id.country_id and picking_company_id.country_id.code or ""),
                          "zipCode": "%s" % (picking_company_id.zip or ""),
                          "city": "%s" % (picking_company_id.city or "")}
                      },
                      "parcels": self.gls_packages_info(total_bulk_weight or False, package_details)
                    }

        return order_data

    def gls_fr_send_shipping(self, pickings):
        for picking in pickings:
            try:
                request_data = self.gls_order_request_data(picking)
                api_url = self.deside_gls_url("/shipments")
                response_data = self.gls_api_calling_function(api_url, request_data)
            except Exception as e:
                raise ValidationError(_("\n Response Data : %s") % (e))
            if response_data.status_code in [200, 201]:
                response_data = response_data.json()
                _logger.info("GLS Response Data : %s" % (response_data))
                tracking_number = []
                if response_data.get("parcels"):
                    for parcel in response_data.get("parcels"):
                        tracking_number.append(parcel.get('trackId'))

                process_message = (_("Shipment created!<br/> <b>Shipment Tracking Number : </b>%s") % (','.join(tracking_number)))
                picking.gls_fr_tracking_url = response_data.get("location")
                if response_data.get("labels"):
                    for label in response_data.get("labels"):
                        label_data = binascii.a2b_base64(str(label))
                        picking.message_post(body=process_message,attachments=[('GLS_Label_%s.pdf' % (self.id), label_data)])
                    shipping_data = {
                                    'exact_price': float(picking.carrier_price or 0.0),
                                    'tracking_number': ','.join(tracking_number)}
                    shipping_data = [shipping_data]
                    return shipping_data
                else:
                    raise ValidationError(_("Response Data : %s ") % (response_data))
            else:
                raise ValidationError(
                    _("Response Code : %s Response Data : %s ") % (response_data.status_code, response_data.text))

    def gls_fr_get_tracking_link(self, picking):
        link = picking.gls_fr_tracking_url
        if link:
            res = '%s' % (picking.gls_fr_tracking_url)
            return res
        raise ValidationError("URL Is Not Available")


    def gls_fr_cancel_shipment(self, picking):
        raise ValidationError("For Cancel GLS Shipment functionality, Please contact Vraja Technologies!")
