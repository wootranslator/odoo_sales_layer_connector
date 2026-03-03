# Temu Odoo 18 Integration

This module provides a robust and professional integration between Odoo 18 (Enterprise & Community) and the Temu Marketplace. Designed for the Spanish market, it handles complex fiscal requirements (SII, OSS), contact deduplication, and automated workflows.

## 🚀 Key Features

*   **Marketplaces Dashboard**: A high-level view of your integration status, pending orders, and shipped packages using a modern Kanban interface.
*   **Order Synchronization**: Automated and manual import of Temu sales orders with custom prefixes (e.g., `TEMU/12345`).
*   **Spanish Fiscal Compliance**:
    *   Full support for **SII (Suministro Inmediato de Información)** and **OSS (One-Stop Shop)**.
    *   Advanced **Tax Mapping** to ensure correct VAT reporting.
    *   Deduplication by **VAT (CIF/NIF)**, email, and name.
*   **Logistics & Tracking**: Automatic synchronization of tracking numbers back to Temu upon validating Odoo pickings.
*   **Workflow Automation**:
    *   **Auto-confirm Paid Orders**: Automatically confirm orders when payment is verified by Temu.
    *   **Payment Registration**: Real-time creation of `account.payment` records with transaction IDs.
*   **Pricing Flexibility**: Choose between using Temu's marketplace prices or Odoo's internal pricelists.
*   **Interactive Onboarding**: Welcome wizard to install dummy data and test the system immediately.

## 🛠 Installation

1.  Copy the `temu_odoo_integration` folder to your Odoo custom addons directory.
2.  Install the dependencies: `sale_management`, `stock`, `delivery`.
3.  Restart Odoo and update the Apps list.
4.  Install the module.

## ⚙️ Configuration

1.  Navigate to **Temu Integration > Configuration > Marketplaces**.
2.  Click **New** to add your Temu API credentials (Client ID, Client Secret).
3.  Define your mappings in the **Mappings** menu:
    *   **SKU Mappings**: Link Temu SKUs to Odoo Products.
    *   **Fiscal Mappings**: Map regions to Odoo Fiscal Positions.
    *   **Payment Mappings**: Link methods to Odoo Payment Journals.
    *   **Tax Mappings**: Map marketplace tax rates to Spanish VAT keys.

## 🧑‍💻 Development

The module is built with clean Odoo 18 API standards and is ready for extending via the built-in hooks.

## 📄 License

Licensed under LGPL-3.
