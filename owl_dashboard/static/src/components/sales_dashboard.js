/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
const { Component } = owl 

export class OwlSalesDashboard extends Component {
    static components = { KpiCard };
}


OwlSalesDashboard.template = "owl_dashboard.OwlSalesDashboard"
OwlSalesDashboard.component = { KpiCard }

registry.category("actions").add("owl.sales_dashboard", OwlSalesDashboard)
