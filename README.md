# tf_l10n_cl — Chile: plan de cuentas e impuestos (TF)

Paquete de localización contable para Odoo 18 que carga el plan de cuentas,
los impuestos y las posiciones fiscales de Chile **sin instalar `l10n_cl` ni
los módulos `l10n_latam_*`**.

Complementa a [`tf_dte_cl`](../tf_dte_cl), el módulo de emisión de DTE ante el
SII, y deja los impuestos de venta listos para emitir.

## Por qué existe

En Odoo 18 el plan de cuentas chileno viene en `l10n_cl`, que instala además
`l10n_latam_base` y `l10n_latam_invoice_document`. Esos módulos agregan a
facturas, diarios y contactos campos como *Tipo de documento* y *Número de
documento*, que `tf_dte_cl` no usa y que llevan a pensar que el folio se ingresa
a mano. Este módulo toma la misma plantilla oficial de Odoo 18 y la entrega sin
esas dependencias.

## Contenido

| Elemento | Detalle |
|---|---|
| Plan de cuentas | 193 cuentas, código de 6 dígitos |
| Grupos de impuestos | IVA 19 %, impuestos específicos, ILA, retenciones de segunda categoría y otras retenciones |
| Impuestos | 28 impuestos de venta y compra, con sus cuentas y etiquetas del reporte |
| Posiciones fiscales | 9 (IVA no recuperable, activo fijo, exentos, entre otras) |
| Reporte de impuestos | Estructura del reporte chileno; crea las etiquetas que usan los impuestos |
| Bancos | 32 bancos de Chile |
| Contactos | Servicio de Impuestos Internos y Tesorería General de la República |

La plantilla se llama **«Chile (TF)»** (código `cl_tf`) para no chocar con la
oficial (`cl`).

### Configuración que deja la plantilla

- Cuenta por cobrar **110310**, por pagar **210210**, ingresos **310115** y gastos **410235**.
- IVA 19 % como impuesto de venta y de compra por defecto.
- Redondeo global de impuestos, contabilidad anglosajona y prefijos de cuentas
  de banco, caja y transferencia.

## Códigos SII de los impuestos de venta

Los impuestos de venta llevan el código SII de `tf_dte_cl` según la tabla 4 del
*Formato de Documentos Tributarios Electrónicos* del SII. Los de compra no llevan
código, porque no se informan en los DTE de venta.

| Impuesto | Tasa | Código SII |
|---|---|---|
| IVA | 19 % | 14 |
| ILA bebidas analcohólicas | 10 % | 27 |
| ILA bebidas con alto contenido de azúcar | 18 % | **271** |
| ILA vinos | 20,5 % | 25 |
| ILA cervezas | 20,5 % | 26 |
| ILA licores | 31,5 % | 24 |

Diferencias con `l10n_cl`:

- El ILA de 18 % tiene el código **271**, como indica el manual del SII.
  `l10n_cl` le asigna el 26, que en el manual corresponde a cervezas (20,5 %).
- Se agrega el **ILA de cervezas** (código 26), que no viene en `l10n_cl`.
- No se incluyen las etiquetas de cuentas e impuestos que solo usa la
  facturación electrónica oficial de Odoo (`l10n_cl_edi`).

## Instalación

Dependencias: `account` y `tf_dte_cl`.

En una base nueva, para que Odoo no instale `l10n_cl` por su cuenta:

1. Crear la base **sin país** (o con uno distinto de Chile) e instalar `tf_dte_cl`.
2. En la compañía: país **Chile** y moneda **CLP**, antes de registrar asientos.
3. Instalar `tf_l10n_cl`.
4. En *Facturación > Ajustes > Localización fiscal*, elegir **Chile (TF)**.

Si el paquete no aparece en el selector, se puede cargar desde la consola de Odoo:

```python
env['account.chart.template'].try_loading('cl_tf', env.company)
env.cr.commit()
```

Odoo permite cambiar el paquete de localización mientras la compañía no tenga asientos.

### Recomendado en Odoo Community

Instalar **`account_usability`** de la OCA (repositorio `account-financial-tools`).
En Community, el plan de cuentas y otros menús contables están ocultos tras el
grupo técnico «Show Full Accounting Features»; ese módulo los muestra.

## Créditos y licencia

Basado en la plantilla contable de `l10n_cl` de Odoo 18 (autor original:
Blanco Martín & Asociados), distribuida bajo LGPL-3.

Licencia: LGPL-3.
