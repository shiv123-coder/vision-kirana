import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "../ThemeToggle"
import { SyncStatusBar } from "./SyncStatusBar"

export function Navbar() {
  return (
    <div className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <SyncStatusBar />
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          {/* Mock Logo */}
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-white font-bold text-xl">V</span>
          </div>
          <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
            VisionKirana
          </span>
        </Link>
        
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <a href="#how-it-works" className="transition-colors hover:text-primary text-muted-foreground">How it Works</a>
          <a href="#intelligence" className="transition-colors hover:text-primary text-muted-foreground">Intelligence</a>
          <a href="#features" className="transition-colors hover:text-primary text-muted-foreground">Features</a>
        </nav>

        <div className="flex items-center gap-4">
          <ThemeToggle />
          <div className="hidden sm:inline-flex">
            <Link to="/login">
              <Button variant="outline">Sign In</Button>
            </Link>
          </div>
          <Link to="/register">
            <Button variant="premium">Get Started</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
