# -*- coding: utf-8 -*-
"""Plantilla de plan de cuentas "Chile (TF)".

Ruta real: models/template_cl_tf.py

Basada en la plantilla oficial de l10n_cl (Odoo 18), sin dependencia de
l10n_cl ni de l10n_latam_*. El código de plantilla es 'cl_tf' para no
chocar con el oficial ('cl').
"""
from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cl_tf')
    def _get_cl_tf_template_data(self):
        return {
            'name': 'Chile (TF)',
            'code_digits': '6',
            'property_account_receivable_id': 'account_110310',
            'property_account_payable_id': 'account_210210',
            'property_account_expense_categ_id': 'account_410235',
            'property_account_income_categ_id': 'account_310115',
            'property_stock_account_input_categ_id': 'account_210230',
            'property_stock_account_output_categ_id': 'account_110640',
            'property_stock_valuation_account_id': 'account_110610',
        }

    @template('cl_tf', 'res.company')
    def _get_cl_tf_res_company(self):
        return {
            self.env.company.id: {
                'anglo_saxon_accounting': True,
                'account_fiscal_country_id': 'base.cl',
                'bank_account_code_prefix': '1101',
                'cash_account_code_prefix': '1101',
                'transfer_account_code_prefix': '117',
                'account_default_pos_receivable_account_id': 'account_110421',
                'income_currency_exchange_account_id': 'account_320265',
                'expense_currency_exchange_account_id': 'account_410195',
                'tax_calculation_rounding_method': 'round_globally',
                'account_sale_tax_id': 'ITAX_19',
                'account_purchase_tax_id': 'OTAX_19',
            },
        }
