<template>
  <div class="min-h-screen bg-black text-green-400 font-mono overflow-hidden relative">
    <Home />
  </div>
</template>

<script setup>
import { useHead } from '@unhead/vue'
import Home from './views/Home.vue'
import { SITE_NAME, SITE_URL, SITE_DESCRIPTION, OG_IMAGE } from './utils/keywords.js'

useHead({
  title: SITE_NAME,
  htmlAttrs: { lang: 'en' },
  meta: [
    { name: 'author', content: 'MatrixScanner' },
    { name: 'robots', content: 'index, follow' },
    { name: 'theme-color', content: '#00ff41' },
    { name: 'color-scheme', content: 'dark' },
  ],
  link: [
    { rel: 'canonical', href: SITE_URL },
  ],
  script: [
    {
      type: 'application/ld+json',
      children: JSON.stringify([
        {
          '@context': 'https://schema.org',
          '@type': 'Organization',
          '@id': SITE_URL + '#organization',
          name: 'MatrixScanner',
          url: SITE_URL,
          logo: SITE_URL.replace(/\/$/, '') + '/Matrix-logo.svg.png',
          sameAs: ['https://github.com/aboodmidani/matrix'],
        },
        {
          '@context': 'https://schema.org',
          '@type': 'WebSite',
          '@id': SITE_URL + '#website',
          name: 'MatrixScanner',
          url: SITE_URL,
          potentialAction: {
            '@type': 'SearchAction',
            target: {
              '@type': 'EntryPoint',
              urlTemplate: SITE_URL + '?scan={search_term_string}',
            },
            'query-input': 'required name=search_term_string',
          },
        },
      ]),
    },
  ],
})
</script>
