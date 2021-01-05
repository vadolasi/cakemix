module.exports = {
  locales: {
    '/': {
      lang: 'en-US',
      title: 'Cakemix',
      description: 'An easy and fast way to create project templates',
    },
    '/pt/': {
      lang: 'pt',
      title: 'Cakemix',
      description: 'Uma maneira fácil e rápida de criar modelos de projeto',
    },
  },

  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }],
  ],

  themeConfig: {
    repo: '',
    editLinks: false,
    docsDir: '',
    editLinkText: '',
    lastUpdated: false,
    locales: {
      '/': {
        label: 'English',
        selectText: 'Languages',
        nav: [
          {
            text: 'Guide',
            link: '/guide/',
          },
        ],
        sidebar: {
          '/guide/': [
            {
              title: 'Guide',
              children: [
                '',
                'cookiecutter',
                'installing',
                'usage',
              ],
            },
          ],
        },
      },
      '/pt/': {
        label: 'Português',
        selectText: 'Idiomas',
        nav: [
          {
            text: 'Guia',
            link: '/pt/guia/',
          },
        ],
        sidebar: {
          '/pt/guia/': [
            {
              title: 'Guia',
              children: [
                '',
                'cookiecutter',
                'instalação',
                'usando',
              ],
            },
          ],
        },
      },
    },
  },

  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
  ],
}
