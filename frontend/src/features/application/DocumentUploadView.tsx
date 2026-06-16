import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileUpload } from "@/components/ui/FileUpload"
import { uploadFile, FileCategory, SpecificType } from "@/services/uploadService"
import { ArrowLeft, CheckCircle2 } from "lucide-react"

export function DocumentUploadView() {
  const { applicationId } = useParams<{ applicationId: string }>()
  const navigate = useNavigate()
  
  const [uploadState, setUploadState] = useState<Record<string, { uploading: boolean, success: boolean, error?: string }>>({})

  const handleUpload = async (file: File, category: FileCategory, type: SpecificType, key: string) => {
    if (!applicationId) return
    
    setUploadState(prev => ({ ...prev, [key]: { uploading: true, success: false } }))
    
    try {
      await uploadFile(file, parseInt(applicationId), category, type)
      setUploadState(prev => ({ ...prev, [key]: { uploading: false, success: true } }))
    } catch (error: any) {
      setUploadState(prev => ({ ...prev, [key]: { uploading: false, success: false, error: error.message } }))
    }
  }

  const getUploadProps = (key: string) => ({
    isUploading: uploadState[key]?.uploading || false,
    isSuccess: uploadState[key]?.success || false,
  })

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Button variant="ghost" onClick={() => navigate("/dashboard")} className="mb-4">
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Dashboard
      </Button>

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-primary">Upload Documents</h1>
        <p className="text-muted-foreground mt-2">
          Please upload the required evidence for Application #{applicationId} to proceed with your loan.
        </p>
      </div>

      <div className="space-y-6">
        {/* Images Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Shop Images</CardTitle>
            <CardDescription>Upload clear photos of your business (Max 5MB each)</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <FileUpload 
                label="Shop Front"
                accept="image/jpeg, image/png, image/webp"
                maxSizeMB={5}
                onFileSelect={(f) => handleUpload(f, "image", "shop_front", "shop_front")}
                {...getUploadProps("shop_front")}
              />
              {uploadState["shop_front"]?.error && <p className="text-xs text-destructive mt-1">{uploadState["shop_front"].error}</p>}
            </div>
            <div>
              <FileUpload 
                label="Shelf Images"
                accept="image/jpeg, image/png, image/webp"
                maxSizeMB={5}
                onFileSelect={(f) => handleUpload(f, "image", "inventory", "shelves")}
                {...getUploadProps("shelves")}
              />
              {uploadState["shelves"]?.error && <p className="text-xs text-destructive mt-1">{uploadState["shelves"].error}</p>}
            </div>
            <div>
              <FileUpload 
                label="Inventory / Stock"
                accept="image/jpeg, image/png, image/webp"
                maxSizeMB={5}
                onFileSelect={(f) => handleUpload(f, "image", "inventory", "stock")}
                {...getUploadProps("stock")}
              />
              {uploadState["stock"]?.error && <p className="text-xs text-destructive mt-1">{uploadState["stock"].error}</p>}
            </div>
          </CardContent>
        </Card>

        {/* Documents Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Financial Documents</CardTitle>
            <CardDescription>Upload PDF invoices or receipts (Max 10MB each)</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <FileUpload 
                label="PDF Invoices"
                accept="application/pdf"
                maxSizeMB={10}
                onFileSelect={(f) => handleUpload(f, "document", "invoice", "invoice")}
                {...getUploadProps("invoice")}
              />
              {uploadState["invoice"]?.error && <p className="text-xs text-destructive mt-1">{uploadState["invoice"].error}</p>}
            </div>
            <div>
              <FileUpload 
                label="Receipts"
                accept="application/pdf"
                maxSizeMB={10}
                onFileSelect={(f) => handleUpload(f, "document", "receipt", "receipt")}
                {...getUploadProps("receipt")}
              />
              {uploadState["receipt"]?.error && <p className="text-xs text-destructive mt-1">{uploadState["receipt"].error}</p>}
            </div>
          </CardContent>
        </Card>

        {/* Audio Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Voice Notes</CardTitle>
            <CardDescription>Upload audio explaining your loan requirement (Max 10MB)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="max-w-md">
              <FileUpload 
                label="Audio Recording"
                accept="audio/mpeg, audio/wav, audio/x-m4a, audio/mp4"
                maxSizeMB={10}
                onFileSelect={(f) => handleUpload(f, "audio", "voice_note", "audio")}
                {...getUploadProps("audio")}
              />
              {uploadState["audio"]?.error && <p className="text-xs text-destructive mt-1">{uploadState["audio"].error}</p>}
            </div>
          </CardContent>
        </Card>
        
        <div className="flex justify-end pt-4">
          <Button variant="premium" size="lg" onClick={() => navigate("/dashboard")}>
            <CheckCircle2 className="w-5 h-5 mr-2" />
            Finish & Submit
          </Button>
        </div>
      </div>
    </div>
  )
}
