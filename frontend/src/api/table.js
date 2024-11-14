import request from '@/utils/request'

export function customer_info(query) {
    return request({
        url: '/dbquery/query_CustomerInfo',
        method: 'get',
        params: query
    })
}

export function custometList(params) {
    return request({
        url: '/dbquery/customerlist',
        method: 'get',
        params
    })
}

/** 
  query: dict
  parm: has_three_level
*/
export function customer_filter(query) {
    return request({
        url: '/dbquery/filter_CustomerInfo',
        method: 'get',
        params: query
    })
}

export function summary_dashboard(params) {
    return request({
        url: '/dbquery/summary_CustomerDashboard',
        method: 'get',
        params
    })
}

export function summary_customer(query) {
    return request({
        url: '/dbquery/summary_CustomerInfo',
        method: 'get',
        params: query
    })
}

export function summary_customerSell(params) {
    return request({
        url: '/dbquery/summary_CustomerSell',
        method: 'get',
        params
    })
}

export function summary_sofoware(query) {
    return request({
        url: '/dbquery/summary_CustomerSoft',
        method: 'get',
        params: query
    })
}

export function summary_rcr(query) {
    return request({
        url: '/dbquery/summary_CustomerRCR',
        method: 'get',
        params: query
    })
}

export function summary_product(query) {
    return request({
        url: '/dbquery/summary_CustomerProduct',
        method: 'get',
        params: query
    })
}

export function summary_network(query) {
    return request({
        url: '/dbquery/summary_CustomerNetwork',
        method: 'get',
        params: query
    })
}

export function summary_financial(query) {
    return request({
        url: '/dbquery/summary_CustomerFinancial',
        method: 'get',
        params: query
    })
}

export function summary_contact(query) {
    return request({
        url: '/dbquery/summary_CustomerContact',
        method: 'get',
        params: query
    })
}

export function my_view_add(query) {
    return request({
        url: '/dbquery/my_view_add',
        method: 'get',
        params: query
    })
}


export function manufactorySoftware(params) {
    return request({
        url: '/dbquery/manufactory_sw',
        method: 'get',
        params
    })
}

export function ontSoftware(params) {
    return request({
        url: '/software-management/ont-software',
        method: 'get',
        params
    })
}

export function nwfSoftware(params) {
    return request({
        url: '/software-management/nwf-software',
        method: 'get',
        params
    })
}

export function mobileSoftware(params) {
    return request({
        url: '/software-management/mobile-software',
        method: 'get',
        params
    })
}

export function trainOntSoftware() {
    return request({
        url: 'dbquery/SW_ONT_info',
        method: 'get',
    })
}

export function trainNWFSoftware() {
    return request({
        url: 'dbquery/SW_NWF_info',
        method: 'get',
    })
}

export function trainNWCCSoftware() {
    return request({
        url: 'dbquery/SW_NWCC_info',
        method: 'get',
    })
}

export function trainMobileSoftware() {
    return request({
        url: 'dbquery/SW_MAPP_info',
        method: 'get',
    })
}

export function trainFWASoftware() {
    return request({
        url: 'dbquery/SW_FWA_info',
        method: 'get',
    })
}

export function goldenInfoSoftware() {
    return request({
        url: 'dbquery/golden_info',
        method: 'get',
    })
}

export function productStatus(params) {
    return request({
        url: 'dbquery/product_status',
        method: 'get',
        params
    })
}

export function MainStreamOverview(params) {
    return request({
        url: 'dbquery/mainstream',
        method: 'get',
        params
    })
}


export function FocRequestStatus(params) {
    return request({
        url: 'dbquery/web_issues_FoC',
        method: 'get',
        params
    })
}

export function DeltaConfigStatus(params) {
    return request({
        url: 'dbquery/delta_configure',
        method: 'get', 
        params
    })
}

export function productNWCCSaaS(params) {
    return request({
        url: '/dbquery/nwcc_info',
        method: 'get',
        params
    })
}

export function productPreconfig(params) {
    return request({
        url: '/dbquery/preconfig_info',
        method: 'get',
        params
    })
}

export function releaseTargetCustomer(params) {
    return request({
        url: 'dbquery/target_customer',
        method: 'get',
        params
    })
}

export function releaseTargetDevice(params) {
    return request({
        url: '/dbquery/target_device',
        method: 'get',
        params
    })
}

export function releaseEnd(params) {
    return request({
        url: 'dbquery/end_to_end',
        method: 'get',
        params
    })
}

export function maintenanceFCUTickets(params) {
    return request({
        url: 'dbquery/fcu_tickets',
        method: 'get',
        params
    })
}

export function maintenanceSalesForce(params) {
    return request({
        url: 'dbquery/salesforce',
        method: 'get',
        params
    })
}

export function adminUserManagement() {
    return request({
        url: 'admin/user-management',
        method: 'get',
    })
}

export function adminGradeManagement(params) {
    return request({
        url: 'user/grade_manage',
        method: 'get',
        params
    })
}

export function adminSupplyChainSum() {
    return request({
        url: 'admin/supply-chain-sum',
        method: 'get',
    })
}

export function adminSupplyChain() {
    return request({
        url: 'admin/supply-chain',
        method: 'get',
    })
}

export function userManage(params) {
    return request({
        url: 'user/user_manage',
        method: 'get',
        params
    })
}

export function getProductList(params) {
    return request({
        url: 'dbquery/device_list',
        method: 'get',
        params
    })
}

export function getReleaseList(params) {
    return request({
        url: 'dbquery/release_list',
        method: 'get',
        params
    })
}

export function getSoftwareOverview(params) {
    return request({
        url: 'dbquery/sw_overview',
        method: 'get',
        params
    })
}

export function getGradeList(params) {
    return request({
        url: 'user/grade_list',
        method: 'get',
        params
    })
}

export function getMyaction(params) {
    return request({
        url: 'dbquery/my_action',
        method: 'get',
        params
    })
}

export function getMyactionRelease(params) {
    return request({
        url: 'dbquery/myaction_release',
        method: 'get',
        params
    })
}

export function refreshActions(params) {
    return request({
        url: 'dbquery/myaction_list',
        method: 'get',
        params
    })
}