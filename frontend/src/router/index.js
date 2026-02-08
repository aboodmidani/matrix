import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DirectoryScan from '../views/DirectoryScan.vue'
import VulnerabilityScan from '../views/VulnerabilityScan.vue'
import DNSScan from '../views/DNSScan.vue'
import PortScan from '../views/PortScan.vue'
import TechnologyScan from '../views/TechnologyScan.vue'
import FirewallScan from '../views/FirewallScan.vue'
import SubdomainScan from '../views/SubdomainScan.vue'
import Results from '../views/Results.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // {
  //   path: '/directory-scan',
  //   name: 'DirectoryScan',
  //   component: DirectoryScan
  // },
  // {
  //   path: '/vulnerability-scan',
  //   name: 'VulnerabilityScan',
  //   component: VulnerabilityScan
  // },
  {
    path: '/dns-scan',
    name: 'DNSScan',
    component: DNSScan
  },
  {
    path: '/port-scan',
    name: 'PortScan',
    component: PortScan
  },
  {
    path: '/technology-scan',
    name: 'TechnologyScan',
    component: TechnologyScan
  },
  {
    path: '/firewall-scan',
    name: 'FirewallScan',
    component: FirewallScan
  },
  {
    path: '/subdomain-scan',
    name: 'SubdomainScan',
    component: SubdomainScan
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router