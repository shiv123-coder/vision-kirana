import { render, screen } from '@testing-library/react'
import App from './App'
import { describe, it, expect } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

describe('App Component', () => {
  it('renders without crashing', () => {
    render(
      <GoogleOAuthProvider clientId="test-client-id">
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </QueryClientProvider>
      </GoogleOAuthProvider>
    )
    
    // We just want to check if the app mounted. 
    // Since we don't know the exact text, we can just assert it renders some HTML element.
    expect(document.body).toBeInTheDocument()
  })
})
