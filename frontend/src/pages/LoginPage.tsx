import { Navbar } from "@/components/layout/Navbar";
import { GoogleLoginButton } from "@/features/auth/GoogleLoginButton";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function LoginPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Welcome Back</CardTitle>
            <CardDescription>Sign in to your VisionKirana account to continue.</CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center pb-8">
            <GoogleLoginButton />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
