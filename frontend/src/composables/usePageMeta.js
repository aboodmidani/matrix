import { useHead, useSeoMeta } from '@unhead/vue'
import { computed } from 'vue'
import { SITE_NAME, SITE_URL, SITE_DESCRIPTION, OG_IMAGE, TWITTER_HANDLE } from '../utils/keywords.js'

export function usePageMeta(options = {}) {
  const {
    title = SITE_NAME,
    description = SITE_DESCRIPTION,
    url = SITE_URL,
    image = OG_IMAGE,
    keywords = '',
  } = options

  useSeoMeta({
    title,
    description,
    keywords,
    ogTitle: title,
    ogDescription: description,
    ogUrl: url,
    ogImage: image,
    ogImageWidth: '512',
    ogImageHeight: '512',
    ogSiteName: SITE_NAME,
    twitterCard: 'summary_large_image',
    twitterTitle: title,
    twitterDescription: description,
    twitterImage: image,
    twitterSite: TWITTER_HANDLE,
  })

  useHead({
    link: [
      { rel: 'canonical', href: url },
    ],
  })
}

export function useScanResultMeta(targetUrl, scanResults) {
  const hasResults = computed(() => {
    return Object.values(scanResults).some(s => s.status === 'done' && s.data)
  })

  const scanTitle = computed(() => {
    if (!targetUrl) return SITE_NAME
    const host = targetUrl.replace(/https?:\/\//, '').replace(/\/.*$/, '')
    return `${host} — Security Scan Results | ${SITE_NAME}`
  })

  const scanDescription = computed(() => {
    if (!hasResults.value) return SITE_DESCRIPTION
    const done = Object.values(scanResults).filter(s => s.status === 'done')
    return `Security scan results for ${targetUrl}: ${done.length} checks completed including DNS, ports, SSL, headers, and more. ${SITE_NAME} web vulnerability assessment.`
  })

  usePageMeta({
    title: scanTitle.value,
    description: scanDescription.value,
    url: targetUrl || SITE_URL,
    keywords: 'security scan results, website audit, vulnerability report',
  })

  return { hasResults, scanTitle, scanDescription }
}
