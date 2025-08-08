import React from 'react';
import { Button } from './ui/button';
import { Download, FileText, FileSpreadsheet } from 'lucide-react';

interface DownloadButtonsProps {
  pdfId: string;
  isProcessing?: boolean;
}

const DownloadButtons: React.FC<DownloadButtonsProps> = ({ pdfId, isProcessing = false }) => {
  const handleDownload = async (format: 'pdf' | 'excel') => {
    try {
      const response = await fetch(`http://localhost:5000/export/${pdfId}/${format}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the filename from the response headers
      const contentDisposition = response.headers.get('content-disposition');
      let filename = `summary_${pdfId}.${format === 'pdf' ? 'pdf' : 'xlsx'}`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Create a blob from the response
      const blob = await response.blob();
      
      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      
      // Trigger the download
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(`Error downloading ${format}:`, error);
      alert(`Failed to download ${format.toUpperCase()} file. Please try again.`);
    }
  };

  return (
    <div className="flex gap-4 mt-6">
      <Button
        onClick={() => handleDownload('pdf')}
        disabled={isProcessing}
        className="flex items-center gap-2 bg-red-600 hover:bg-red-700"
      >
        <FileText className="w-4 h-4" />
        Download PDF
      </Button>
      
      <Button
        onClick={() => handleDownload('excel')}
        disabled={isProcessing}
        className="flex items-center gap-2 bg-green-600 hover:bg-green-700"
      >
        <FileSpreadsheet className="w-4 h-4" />
        Download Excel
      </Button>
    </div>
  );
};

export default DownloadButtons;
