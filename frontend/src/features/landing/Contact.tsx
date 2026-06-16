import { Button } from "@/components/ui/button"

export function Contact() {
  return (
    <section className="py-24 bg-background relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-primary/10 rounded-full blur-[100px] pointer-events-none -z-10" />
      
      <div className="container mx-auto px-4 md:px-8">
        <div className="max-w-4xl mx-auto bg-card border rounded-3xl p-8 md:p-16 shadow-2xl relative z-10 overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-full blur-3xl -z-10 translate-x-1/2 -translate-y-1/2" />
          
          <div className="text-center mb-10">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">Ready to Transform Your Underwriting?</h2>
            <p className="text-lg text-muted-foreground">Request a demo or get access to our API documentation.</p>
          </div>

          <form className="max-w-md mx-auto space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">First Name</label>
                <input type="text" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all" placeholder="John" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Last Name</label>
                <input type="text" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all" placeholder="Doe" />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Work Email</label>
              <input type="email" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all" placeholder="john@bank.com" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Company</label>
              <input type="text" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all" placeholder="Finance Corp" />
            </div>
            <Button variant="premium" className="w-full mt-4 h-12 text-md">Request Access</Button>
          </form>
        </div>
      </div>
    </section>
  )
}
