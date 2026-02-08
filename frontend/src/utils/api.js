import { ref } from 'vue'

// Get API URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Security configuration
const SECURITY_CONFIG = {
  timeout: 30000,
  maxRetries: 3,
  retryDelay: 1000
}

export class ApiService {
  constructor() {
    this.baseURL = API_URL
    this.requestCount = 0
    this.lastRequestTime = 0
  }

  // Rate limiting implementation
  async checkRateLimit() {
    const now = Date.now()
    if (now - this.lastRequestTime < 1000) {
      this.requestCount++
      if (this.requestCount > 5) {
        throw new Error('Rate limit exceeded. Please wait before making more requests.')
      }
    } else {
      this.requestCount = 1
    }
    this.lastRequestTime = now
  }

  // Enhanced request method with security features
  async makeRequest(endpoint, options = {}) {
    try {
      // Rate limiting
      await this.checkRateLimit()

      // Input validation
      if (!endpoint || typeof endpoint !== 'string') {
        throw new Error('Invalid endpoint')
      }

      // Security headers
      const headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Client-Version': '3.0.0',
        ...options.headers
      }

      // Remove any potentially dangerous headers
      delete headers['Authorization']
      delete headers['Cookie']

      const config = {
        ...options,
        headers,
        signal: AbortSignal.timeout(SECURITY_CONFIG.timeout)
      }

      const response = await fetch(`${this.baseURL}${endpoint}`, config)

      // Security checks
      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`HTTP ${response.status}: ${errorText || 'Request failed'}`)
      }

      // Content-Type validation
      const contentType = response.headers.get('content-type')
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Invalid response format')
      }

      const data = await response.json()
      
      // Output sanitization
      return this.sanitizeResponse(data)
      
    } catch (error) {
      console.error('API request failed:', error)
      
      // Security: Don't expose internal error details to frontend
      if (error.name === 'AbortError') {
        throw new Error('Request timeout. Please try again.')
      } else if (error.message.includes('HTTP')) {
        throw error
      } else {
        throw new Error('Network error. Please check your connection.')
      }
    }
  }

  // Response sanitization
  sanitizeResponse(data) {
    if (!data || typeof data !== 'object') {
      return data
    }

    const sanitized = JSON.parse(JSON.stringify(data))
    
    // Remove potentially dangerous properties
    const dangerousProps = ['__proto__', 'constructor', 'prototype']
    dangerousProps.forEach(prop => {
      if (sanitized[prop]) {
        delete sanitized[prop]
      }
    })

    return sanitized
  }

  async get(endpoint) {
    return this.makeRequest(endpoint, {
      method: 'GET'
    })
  }

  async post(endpoint, data) {
    return this.makeRequest(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async postForm(endpoint, formData) {
    // For form data, we need different handling
    try {
      await this.checkRateLimit()
      
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'POST',
        body: formData,
        signal: AbortSignal.timeout(SECURITY_CONFIG.timeout)
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Request failed`)
      }

      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json()
        return this.sanitizeResponse(data)
      }
      
      return response
      
    } catch (error) {
      console.error('Form request failed:', error)
      throw new Error('Form submission failed. Please try again.')
    }
  }

  async downloadReport(results, scanType) {
    try {
      if (!results || !scanType) {
        throw new Error('Invalid download parameters')
      }

      const response = await fetch(`${this.baseURL}/download-results`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
          results,
          scan_type: scanType
        }),
        signal: AbortSignal.timeout(SECURITY_CONFIG.timeout)
      })

      if (!response.ok) {
        throw new Error('Download failed')
      }

      const blob = await response.blob()
      
      // Security: Validate file type
      if (!blob.type || !blob.type.includes('text/plain')) {
        throw new Error('Invalid file type')
      }

      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `scan_results_${scanType}_${Date.now()}.txt`
      
      // Security: Validate filename
      const safeFilename = a.download.replace(/[^a-zA-Z0-9._-]/g, '_')
      a.download = safeFilename
      
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      return true
    } catch (error) {
      console.error('Download failed:', error)
      throw new Error('Failed to download report. Please try again.')
    }
  }

  // Health check method
  async healthCheck() {
    try {
      const response = await this.get('/health')
      return response.status === 'healthy'
    } catch (error) {
      return false
    }
  }

  // Get API info
  async getAPIInfo() {
    try {
      return await this.get('/')
    } catch (error) {
      throw new Error('Unable to connect to API')
    }
  }

  // Subdomain scan
  async scanSubdomains(url) {
    try {
      if (!url || typeof url !== 'string') {
        throw new Error('Invalid URL provided')
      }

      const formData = new URLSearchParams()
      formData.append('url', url)

      return await this.postForm('/scan/subdomains', formData)
    } catch (error) {
      console.error('Subdomain scan failed:', error)
      throw new Error('Subdomain scan failed. Please try again.')
    }
  }
}

// Create singleton instance
export const apiService = new ApiService()

// Composable for reactive API state
export function useApi() {
  const loading = ref(false)
  const error = ref(null)
  const lastError = ref(null)

  const executeRequest = async (requestFn) => {
    loading.value = true
    error.value = null

    try {
      const result = await requestFn()
      lastError.value = null
      return result
    } catch (err) {
      error.value = err.message
      lastError.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
    lastError.value = null
  }

  return {
    loading,
    error,
    lastError,
    executeRequest,
    clearError
  }
}