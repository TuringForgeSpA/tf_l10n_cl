# -*- coding: utf-8 -*-
"""Plantilla "Chile (TF)": carga, configuración de la compañía, impuestos y reporte.

Ruta real: tests/test_chart.py

Carga la plantilla en una compañía nueva, igual que al elegir "Chile (TF)" en
Localización fiscal, y verifica los valores contra los datos de la plantilla.
"""
from odoo.tests import TransactionCase, tagged

from odoo.addons.tf_dte_cl.models.dte_lines import tax_config_errors

TEMPLATE = 'cl_tf'
# Códigos SII de los impuestos de venta (los de compra no los necesitan).
SALE_SII_CODES = {
    'ITAX_19': '14',
    'ila_a_100_s': '27',
    'ila_a_180_s': '271',
    'ila_v_205_s': '25',
    'ila_l_315_s': '24',
    'ila_c_205_s': '26',
}
WITHHOLDINGS = {
    'I_IU2C': -10.75, 'I_IR2C_2021': -11.5, 'I_IR2C_2022': -12.25, 'I_IR2C_2023': -13.0,
    'I_IR2C_2024': -13.75, 'I_IR2C_2025': -14.5, 'I_IR2C_2026': -15.25,
}
INACTIVE = ('I_IU2C', 'I_IR2C_2021')


@tagged('post_install', '-at_install', 'tf_l10n_cl')
class TestChartTemplate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({
            'name': 'Chile TF Prueba SpA',
            'country_id': cls.env.ref('base.cl').id,
            'currency_id': cls.env.ref('base.CLP').id,
        })
        cls.env.user.company_ids |= cls.company
        cls.Template = cls.env['account.chart.template'].with_company(cls.company)
        cls.Template.try_loading(TEMPLATE, cls.company, install_demo=False)
        cls.data = cls.env['account.chart.template']._get_chart_template_data(TEMPLATE)

    def ref(self, xmlid):
        return self.Template.ref(xmlid, raise_if_not_found=False)

    # --- carga completa -------------------------------------------------------
    def test_template_loaded(self):
        self.assertEqual(self.company.chart_template, TEMPLATE)
        for model in ('account.account', 'account.tax', 'account.tax.group', 'account.fiscal.position'):
            missing = [xmlid for xmlid in self.data[model] if not self.ref(xmlid)]
            with self.subTest(model=model):
                self.assertFalse(missing, 'Registros de la plantilla que no se crearon: %s' % missing[:10])
        self.assertEqual(len(self.data['account.account']), 193)
        self.assertEqual(len(self.data['account.tax']), 28)
        self.assertEqual(len(self.data['account.fiscal.position']), 9)

    def test_company_configuration(self):
        company = self.company
        self.assertEqual(company.account_sale_tax_id, self.ref('ITAX_19'))
        self.assertEqual(company.account_purchase_tax_id, self.ref('OTAX_19'))
        self.assertEqual(company.tax_calculation_rounding_method, 'round_globally')
        self.assertEqual(company.account_fiscal_country_id, self.env.ref('base.cl'))
        self.assertTrue(company.anglo_saxon_accounting)
        partner = self.env['res.partner'].with_company(company).create({'name': 'Cliente cuentas por defecto'})
        self.assertEqual(partner.property_account_receivable_id, self.ref('account_110310'))
        self.assertEqual(partner.property_account_payable_id, self.ref('account_210210'))

    # --- impuestos --------------------------------------------------------------
    def test_sale_taxes_sii_codes(self):
        for xmlid, code in SALE_SII_CODES.items():
            with self.subTest(tax=xmlid):
                tax = self.ref(xmlid)
                self.assertEqual((tax.type_tax_use, tax.tf_dte_cl_sii_code), ('sale', code))

    def test_sale_taxes_valid_for_dte(self):
        # Los impuestos de venta deben cumplir las reglas del DTE de tf_dte_cl (código, tasa, sin precio incluido).
        for xmlid in SALE_SII_CODES:
            with self.subTest(tax=xmlid):
                self.assertFalse(tax_config_errors(self.ref(xmlid)._tf_dte_cl_info()))

    def test_withholdings(self):
        for xmlid, amount in WITHHOLDINGS.items():
            with self.subTest(tax=xmlid):
                tax = self.ref(xmlid)
                self.assertEqual((tax.type_tax_use, tax.amount), ('purchase', amount))
                self.assertEqual(tax.active, xmlid not in INACTIVE)

    def test_tax_computation(self):
        iva = self.ref('ITAX_19').compute_all(10000.0, currency=self.company.currency_id)
        self.assertEqual((iva['total_excluded'], iva['total_included']), (10000.0, 11900.0))
        fees = self.ref('I_IR2C_2026').compute_all(100000.0, currency=self.company.currency_id)
        self.assertEqual(fees['total_included'], 84750.0)                # retención 15,25 %

    def test_taxes_have_group_and_report_tags(self):
        self.assertTrue(all(self.ref(xmlid).tax_group_id for xmlid in self.data['account.tax']))
        sale = self.ref('ITAX_19')
        base_tags = sale.invoice_repartition_line_ids.filtered(lambda l: l.repartition_type == 'base').tag_ids
        self.assertIn('+Ventas Netas Gravadas con IVA', base_tags.mapped('name'))

    def test_tax_report(self):
        report = self.env.ref('tf_l10n_cl.tax_report')
        self.assertEqual(report.country_id, self.env.ref('base.cl'))
        self.assertTrue(report.line_ids)

    # --- datos del módulo -------------------------------------------------------
    def test_banks(self):
        banks = self.env['ir.model.data'].search_count([('module', '=', 'tf_l10n_cl'), ('model', '=', 'res.bank')])
        self.assertEqual(banks, 32)

    def test_official_localization_not_installed(self):
        # El paquete existe para no depender de la localización oficial.
        modules = self.env['ir.module.module'].search([
            ('name', 'in', ('l10n_cl', 'l10n_latam_base', 'l10n_latam_invoice_document')),
            ('state', '=', 'installed'),
        ])
        self.assertFalse(modules, 'No deben estar instalados: %s' % ', '.join(modules.mapped('name')))
