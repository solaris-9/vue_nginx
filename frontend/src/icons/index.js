//import SvgIcon from '@/components/SvgIcon'// svg component

const req = require.context('@/icons/svg/', false, /.*/)
/* const req = require.context('./svg', false, /\.svg$/) */
const requireAll = requireContext => requireContext.keys().map(requireContext)
requireAll(req)
//req.keys().forEach((SvgIcon) => req(SvgIcon))

/* export default (app) => {
    app.component('svg-icon', SvgIcon)
}
 */