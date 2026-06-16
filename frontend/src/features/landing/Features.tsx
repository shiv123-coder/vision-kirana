import { motion } from "framer-motion"
import { Check } from "lucide-react"

const features = [
  "Offline-first PWA Support",
  "Role-Based Access Control",
  "Bank-Grade Encryption",
  "Regional Language Support",
  "Automated Document Validation",
  "Customizable Scoring Models",
  "Real-time Dashboard Analytics",
  "API Integrations for NBFCs"
]

export function Features() {
  return (
    <section id="features" className="py-24 bg-card border-y">
      <div className="container mx-auto px-4 md:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-5xl font-bold mb-6">Built for Scale & Security</h2>
            <p className="text-lg text-muted-foreground mb-8">
              Whether you are a microfinance institution deploying loan officers to remote villages, or an NBFC integrating via API, VisionKirana provides the enterprise-grade foundation you need.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {features.map((feature, i) => (
                <div key={i} className="flex items-center gap-2">
                  <div className="w-5 h-5 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                    <Check className="w-3 h-3 text-primary" />
                  </div>
                  <span className="text-sm font-medium text-foreground">{feature}</span>
                </div>
              ))}
            </div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative"
          >
            {/* Mock Dashboard Representation */}
            <div className="aspect-[4/3] rounded-2xl bg-background border shadow-2xl p-4 overflow-hidden relative">
              <div className="w-full h-8 border-b flex items-center gap-2 mb-4">
                <div className="w-3 h-3 rounded-full bg-destructive" />
                <div className="w-3 h-3 rounded-full bg-warning" />
                <div className="w-3 h-3 rounded-full bg-success" />
              </div>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="h-20 bg-card border rounded-lg" />
                <div className="h-20 bg-card border rounded-lg" />
                <div className="h-20 bg-card border rounded-lg" />
              </div>
              <div className="h-40 bg-card border rounded-lg w-full mb-4 relative overflow-hidden">
                 <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-primary/20 to-transparent" />
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
