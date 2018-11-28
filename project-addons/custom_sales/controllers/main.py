# -*- coding: utf-8 -*-
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        """
        Skip payment step. Just confirm order because customers pay on store.
        :param post: post args
        :return: redirect to confirmation step
        """
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        order.onchange_partner_shipping_id()
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        request.website.sale_get_order(update_pricelist=True)

        # Do not need extra info
        # extra_step = request.env.ref('website_sale.extra_info_option')
        # if extra_step.active:
        #     return request.redirect("/shop/extra_info")

        # Pass order to state sent like a real payment
        order.state = 'sent'

        # Redirect to confirmation directly skipping payment step
        return request.redirect("/shop/confirmation")

