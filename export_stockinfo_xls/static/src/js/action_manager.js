///** @odoo-module */
//import { registry } from "@web/core/registry";
//import { download } from "@web/core/network/download";
//import { BlockUI } from "@web/core/ui/block_ui";
//// This function is responsible for generating and downloading an XLSX report.
//registry.category("ir.actions.report handlers").add("stock_xlsx", async (action) => {
//    if (action.report_type === 'stock_xlsx') {
//        const blockUI = new BlockUI();
//        await download({
//            url: '/xlsx_reports',
//            data: action.data,
//            complete: () => unblockUI,
//            error: (error) => self.call('crash_manager', 'rpc_error', error),
//        });
//    }
//});




//** @odoo-module */
//
//import { registry } from "@web/core/registry";
//import { download } from "@web/core/network/download";
//import { useService } from "@web/core/utils/hooks";
//import { BlockUI } from "@web/core/ui/block_ui";
//
//// Register handler for stock_xlsx report type
//registry.category("ir.actions.report handlers").add("stock_xlsx", async (action, options, env) => {
//    if (action.report_type === 'stock_xlsx') {
//        // Create BlockUI instance
//        const blockUI = new BlockUI();
//        try {
//            // Block the UI while downloading
//            blockUI.mount(document.body);
//
//            // Attempt to download the report
//            await download({
//                url: '/xlsx_reports',
//                data: action.data,
//            });
//
//            return true; // Indicate that the action was handled
//        } catch (error) {
//            // Get notification service for error handling
//            const notification = env.services.notification;
//            notification.add(error.message, {
//                type: 'danger',
//                sticky: false,
//                title: 'XLSX Report Error'
//            });
//
//            return false; // Indicate action handling failed
//        } finally {
//            // Always ensure UI is unblocked
//            blockUI.destroy();
//        }
//    }
//
//    return false; // Let other handlers process different report types
//});



/** @odoo-module */

import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import { BlockUI } from "@web/core/ui/block_ui";

// Register handler for stock_xlsx report type
registry.category("ir.actions.report handlers").add("stock_xlsx", function (action, options, env) {
    if (action.report_type === 'stock_xlsx') {
        var blockUI = new BlockUI();

        return new Promise(function(resolve, reject) {
            try {
                // Block the UI while downloading
                blockUI.mount(document.body);

                // Prepare the data to send to the controller
                var data = {
                    model: action.model,
                    options: JSON.stringify(action.data || {}),
                    report_name: action.report_name || 'stock_report'
                };

                // Attempt to download the report
                download({
                    url: '/xlsx_reports',
                    data: data,
                    complete: function() {
                        blockUI.destroy();
                        resolve(true);
                    },
                    error: function(error) {
                        // Handle error with notification
                        env.services.notification.add(
                            error.message || "Failed to generate report",
                            {
                                type: 'danger',
                                sticky: false,
                                title: 'XLSX Report Error'
                            }
                        );
                        blockUI.destroy();
                        resolve(false);
                    }
                });

            } catch (error) {
                // Handle any synchronous errors
                env.services.notification.add(
                    error.message || "Failed to generate report",
                    {
                        type: 'danger',
                        sticky: false,
                        title: 'XLSX Report Error'
                    }
                );
                blockUI.destroy();
                resolve(false);
            }
        });
    }

    return false; // Let other handlers process different report types
});