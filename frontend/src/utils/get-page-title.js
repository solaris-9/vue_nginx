import defaultSettings from '@/settings'

const title = defaultSettings.title || 'BBD Customer'

export default function getPageTitle(pageTitle) {
    if (pageTitle) {
        return `${title}`
    }
    return `${title}`
}