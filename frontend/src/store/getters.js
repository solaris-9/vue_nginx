const getters = {
    sidebar: state => state.app.sidebar,
    device: state => state.app.device,
    token: state => state.user.token,
    auth: state => state.user.auth,
    avatar: state => state.user.avatar,
    name: state => state.user.name,
    roles: state => state.user.roles,
    mail: state => state.user.mail,
    level: state => state.user.level,
    permission_routes: state => state.permission.routes,
    perm_data: state => state.permission.permData,
    visitedViews: state => state.tagsView.visitedViews,
    cachedViews: state => state.tagsView.cachedViews,
    customer_list: state => state.settings.customerList,
    product_list: state => state.settings.productList,
    release_list: state => state.settings.releaseList,
}

export default getters