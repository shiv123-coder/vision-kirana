import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { PlusCircle, Edit, Store, Activity, IndianRupee, TrendingUp } from "lucide-react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface Application {
  id: number
  status: string
  requested_amount: number
  purpose: string | null
}

interface Shop {
  id: number
  shop_name: string
  owner_name: string
  mobile: string
  address: string
  city: string
  state: string
  category: string
  years_in_business: number
  monthly_sales: number
  applications?: Application[]
}

export function ShopDashboard() {
  const [shops, setShops] = useState<Shop[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    const fetchShops = async () => {
      try {
        const token = localStorage.getItem("access_token")
        if (!token) {
            setError("Authentication required.")
            setLoading(false)
            return
        }

        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/api/v1/shops/`", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        })

        if (!response.ok) {
          throw new Error("Failed to load shops")
        }

        const data = await response.json()
        setShops(data)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchShops()
  }, [])

  if (loading) {
    return <div className="p-8 text-center">Loading your shops...</div>
  }

  if (error) {
    return <div className="p-8 text-center text-destructive">{error}</div>
  }

  const healthData = [
    { month: 'Jan', score: 65 },
    { month: 'Feb', score: 68 },
    { month: 'Mar', score: 74 },
    { month: 'Apr', score: 79 },
    { month: 'May', score: 85 },
  ]

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">My Business</h1>
          <p className="text-muted-foreground mt-2">Manage your shop profile and view AI insights.</p>
        </div>
        <Button onClick={() => navigate("/register-shop")} variant="premium">
          <PlusCircle className="mr-2 h-4 w-4" />
          Add New Shop
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Business Health Score</CardTitle>
            <Activity className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-600">85 / 100</div>
            <p className="text-xs text-muted-foreground">Excellent condition</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Applications</CardTitle>
            <Store className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1</div>
            <p className="text-xs text-muted-foreground">In review phase</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Estimated Loan Limit</CardTitle>
            <IndianRupee className="h-4 w-4 text-indigo-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹2.5L</div>
            <p className="text-xs text-muted-foreground">Based on AI assessment</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="col-span-1 lg:col-span-2">
          <CardHeader>
            <CardTitle>Health Trend</CardTitle>
            <CardDescription>Your business health score over the last 5 months.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={healthData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} className="stroke-muted" />
                  <XAxis dataKey="month" tickLine={false} axisLine={false} className="text-xs" />
                  <YAxis domain={[0, 100]} tickLine={false} axisLine={false} className="text-xs" />
                  <Tooltip contentStyle={{ borderRadius: '8px', border: '1px solid hsl(var(--border))', backgroundColor: 'hsl(var(--background))' }} />
                  <Line type="monotone" dataKey="score" stroke="#10b981" strokeWidth={3} dot={{ r: 4, fill: "#10b981" }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Registered Shops</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {shops.length === 0 ? (
              <div className="text-center py-6 text-muted-foreground">
                <Store className="w-12 h-12 mx-auto mb-3 opacity-20" />
                <p>No shops registered yet.</p>
              </div>
            ) : (
              shops.map(shop => (
                <div key={shop.id} className="p-4 border rounded-xl hover:bg-muted/50 transition-colors">
                  <h3 className="font-semibold text-lg">{shop.shop_name}</h3>
                  <p className="text-sm text-muted-foreground mb-4">{shop.address}, {shop.city}</p>
                  <Button variant="outline" size="sm" className="w-full" onClick={() => navigate(`/shops/${shop.id}/edit`)}>
                    <Edit className="w-4 h-4 mr-2" />
                    Manage Application
                  </Button>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
