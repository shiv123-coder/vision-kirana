export type FileCategory = "image" | "document" | "audio"
export type SpecificType = 
  | "shop_front" 
  | "inventory" 
  | "invoice" 
  | "receipt" 
  | "voice_note" 
  | "other"

export interface UploadResponse {
  message: string
  id: number
  url: string
}

export const uploadFile = async (
  file: File,
  applicationId: number,
  fileCategory: FileCategory,
  specificType: SpecificType
): Promise<UploadResponse> => {
  const token = localStorage.getItem("access_token")
  
  if (!token) {
    throw new Error("Authentication required for upload")
  }

  const formData = new FormData()
  formData.append("file", file)
  formData.append("application_id", applicationId.toString())
  formData.append("file_category", fileCategory)
  formData.append("specific_type", specificType)

  const response = await fetch("/api/v1/upload/", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    },
    body: formData
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw new Error(errorData?.detail || "Failed to upload file")
  }

  return response.json()
}
