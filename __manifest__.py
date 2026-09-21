# -*- coding: utf-8 -*-
{
    'name': 'Chile - Plan de cuentas e impuestos (TF)',
    'summary': 'Plan de cuentas, impuestos, posiciones fiscales y reporte de impuestos para Chile, '
               'sin l10n_cl ni l10n_latam.',
    'version': '18.0.1.0.0',
    'description': 'Plan de cuentas, impuestos y posiciones fiscales de Chile sin l10n_cl ni '
                   'l10n_latam. Ver README.md para la documentación completa.',
    'category': 'Accounting/Localizations/Account Charts',
    'countries': ['cl'],
    'license': 'LGPL-3',
    'author': 'TF',
    'depends': [
        'account',
        'tf_dte_cl',
    ],
    'data': [
        'data/account_tax_report_data.xml',
        'data/res.bank.csv',
        'data/res_partner.xml',
    ],
    'installable': True,
    'application': False,
}
