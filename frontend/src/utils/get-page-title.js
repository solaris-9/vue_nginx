import defaultSettings from '@/settings'

const title = defaultSettings.title || 'BBD Device Deployment'

export default function getPageTitle(pageTitle) {
    if (pageTitle) {
        return `${title}`
    }
    return `${title}`
}