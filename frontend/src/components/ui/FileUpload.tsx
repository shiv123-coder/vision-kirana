import { useState, useRef, ChangeEvent, DragEvent } from "react"
import { UploadCloud, File as FileIcon, X, CheckCircle } from "lucide-react"
import { Button } from "./button"
import { cn } from "@/lib/utils"

interface FileUploadProps {
  accept: string
  maxSizeMB: number
  onFileSelect: (file: File) => void
  label?: string
  description?: string
  isUploading?: boolean
  isSuccess?: boolean
  className?: string
}

export function FileUpload({
  accept,
  maxSizeMB,
  onFileSelect,
  label = "Upload File",
  description,
  isUploading = false,
  isSuccess = false,
  className
}: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const validateFile = (file: File): boolean => {
    setError(null)
    
    // Check size
    if (file.size > maxSizeMB * 1024 * 1024) {
      setError(`File size must be less than ${maxSizeMB}MB`)
      return false
    }

    // Check type (simplified check based on accept string like "image/*" or "application/pdf")
    const acceptTypes = accept.split(",").map(t => t.trim())
    const fileType = file.type
    
    let isValidType = false
    for (const type of acceptTypes) {
      if (type.endsWith("/*")) {
        const baseType = type.split("/")[0]
        if (fileType.startsWith(`${baseType}/`)) {
          isValidType = true
          break
        }
      } else if (fileType === type || file.name.endsWith(type)) {
        isValidType = true
        break
      }
    }

    if (!isValidType) {
      setError(`Invalid file type. Accepted: ${accept}`)
      return false
    }

    return true
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (validateFile(file)) {
        setSelectedFile(file)
        onFileSelect(file)
      }
    }
  }

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (validateFile(file)) {
        setSelectedFile(file)
        onFileSelect(file)
      }
    }
  }

  const onButtonClick = () => {
    inputRef.current?.click()
  }

  const clearFile = () => {
    setSelectedFile(null)
    setError(null)
    if (inputRef.current) {
      inputRef.current.value = ""
    }
  }

  return (
    <div className={cn("w-full", className)}>
      {label && <label className="block text-sm font-medium mb-2">{label}</label>}
      
      {!selectedFile || error ? (
        <div 
          className={cn(
            "relative border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center transition-colors",
            dragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:border-primary/50",
            error ? "border-destructive bg-destructive/5" : ""
          )}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={inputRef}
            type="file"
            accept={accept}
            onChange={handleChange}
            className="hidden"
          />
          
          <UploadCloud className={cn("w-10 h-10 mb-3", error ? "text-destructive" : "text-muted-foreground")} />
          
          <p className="mb-1 text-sm text-center">
            <span className="font-semibold text-primary cursor-pointer hover:underline" onClick={onButtonClick}>
              Click to upload
            </span>{" "}
            or drag and drop
          </p>
          
          <p className="text-xs text-muted-foreground text-center">
            {description || `Accepted: ${accept} (Max ${maxSizeMB}MB)`}
          </p>
          
          {error && <p className="mt-3 text-sm text-destructive font-medium">{error}</p>}
        </div>
      ) : (
        <div className="border rounded-lg p-4 flex items-center justify-between bg-card">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="p-2 bg-primary/10 rounded-md text-primary shrink-0">
              {isSuccess ? <CheckCircle className="w-5 h-5 text-green-500" /> : <FileIcon className="w-5 h-5" />}
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium truncate">{selectedFile.name}</p>
              <p className="text-xs text-muted-foreground">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
              </p>
            </div>
          </div>
          
          {!isUploading && !isSuccess && (
            <Button variant="ghost" size="icon" onClick={clearFile} className="shrink-0 text-muted-foreground hover:text-destructive">
              <X className="w-4 h-4" />
            </Button>
          )}
          
          {isUploading && (
            <div className="text-xs font-medium text-primary animate-pulse">Uploading...</div>
          )}
          
          {isSuccess && (
            <div className="text-xs font-medium text-green-500">Done</div>
          )}
        </div>
      )}
    </div>
  )
}
