import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';
import { CompanyDetails } from './CompanyDetailsForm';

interface FileUploadProps {
  onProcessingComplete?: (pdfId: string) => void;
  companyDetails?: CompanyDetails;
}

const FileUpload: React.FC<FileUploadProps> = ({ onProcessingComplete, companyDetails }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(prev => [...prev, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  // Function to truncate filename for display
  const truncateFilename = (filename: string, maxLength: number = 40) => {
    if (filename.length <= maxLength) return filename;
    
    const extension = filename.split('.').pop();
    const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
    const truncatedName = nameWithoutExt.substring(0, maxLength - 10) + '...';
    
    return `${truncatedName}.${extension}`;
  };

  const processFiles = async () => {
    if (files.length === 0) return;

    setIsProcessing(true);
    setUploadProgress(0);

    try {
      // Step 1: Upload and process PDFs with company details
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files[]', file);
      });
      
      // Add company details to form data if available
      if (companyDetails) {
        formData.append('companyDetails', JSON.stringify(companyDetails));
      }

      const processResponse = await fetch('http://localhost:5000/process', {
        method: 'POST',
        body: formData,
      });

      if (!processResponse.ok) {
        throw new Error(`Processing failed: ${processResponse.statusText}`);
      }

      const processResult = await processResponse.json();
      setUploadProgress(50);

      // Step 2: Save to MongoDB - send all filenames and company details
      const savePayload = {
        filename: files.map(f => f.name).join(', '), // Send all filenames
        summary: processResult,
        companyDetails: companyDetails // Include company details
      };

      const saveResponse = await fetch('http://localhost:5000/save_summary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(savePayload),
      });

      if (!saveResponse.ok) {
        throw new Error(`Saving failed: ${saveResponse.statusText}`);
      }

      const saveResult = await saveResponse.json();
      setUploadProgress(100);

      console.log('Processing complete:', saveResult);
      
      // Navigate to result page with PDF ID
      if (onProcessingComplete) {
        onProcessingComplete(saveResult.pdf_id);
      } else {
        navigate('/result', { state: { pdfId: saveResult.pdf_id } });
      }

    } catch (error) {
      console.error('Error processing files:', error);
      alert('Error processing files. Please try again.');
    } finally {
      setIsProcessing(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
          isDragActive
            ? 'border-primary bg-primary/5'
            : 'border-muted-foreground/25 hover:border-primary/50'
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
        <p className="text-lg font-medium mb-2">
          {isDragActive ? 'Drop CERSAI PDF files here' : 'Drag & drop CERSAI PDF files here'}
        </p>
        <p className="text-sm text-muted-foreground">
          or click to browse files (Multiple PDFs supported)
        </p>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-medium">Selected Files:</h3>
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-muted rounded-lg hover:bg-muted/80 transition-colors"
            >
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <FileText className="w-5 h-5 text-primary flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div 
                    className="font-medium truncate" 
                    title={file.name}
                  >
                    {truncateFilename(file.name)}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </div>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeFile(index)}
                disabled={isProcessing}
                className="flex-shrink-0 ml-2"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          ))}
        </div>
      )}

      {/* Progress Bar */}
      {isProcessing && (
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Processing files...</span>
            <span>{uploadProgress}%</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Process Button */}
      {files.length > 0 && (
        <div className="space-y-4">
          {/* Company Details Summary */}
          {companyDetails && (
            <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <div className="text-sm">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-primary">Processing for:</span>
                  <span className="text-muted-foreground">{companyDetails.companyName}</span>
                </div>
                <div className="flex justify-between items-center mt-1">
                  <span className="text-muted-foreground">CIN:</span>
                  <span className="text-muted-foreground">{companyDetails.cinNumber}</span>
                </div>
              </div>
            </div>
          )}
          
          <Button
            onClick={processFiles}
            disabled={isProcessing}
            className="w-full h-12 text-lg font-medium"
          >
            {isProcessing ? 'Processing...' : `Submit & Process ${files.length} File${files.length > 1 ? 's' : ''}`}
          </Button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;