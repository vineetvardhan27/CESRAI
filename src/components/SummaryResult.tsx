import { Download, Table, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate, useLocation } from 'react-router-dom';
import DownloadButtons from './DownloadButtons';

export const SummaryResult = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get PDF ID from navigation state or use a fallback
  const pdfId = location.state?.pdfId || "123456789";

  const handleBackToUpload = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="max-w-md mx-auto text-center space-y-8">
        {/* Header */}
        <div className="animate-fade-in">
          <h1 className="text-4xl font-bold text-foreground mb-4">Processing Complete!</h1>
          <p className="text-muted-foreground">Your PDF summary is ready for download</p>
          {pdfId && (
            <p className="text-sm text-muted-foreground mt-2">
              Document ID: {pdfId}
            </p>
          )}
        </div>
        
        {/* Download Buttons */}
        <div className="space-y-4 animate-scale-in">
          <DownloadButtons pdfId={pdfId} />
        </div>
        
        {/* Back Button */}
        <div className="pt-6 animate-fade-in">
          <Button
            variant="ghost"
            onClick={handleBackToUpload}
            className="text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Process More Files
          </Button>
        </div>
      </div>
    </div>
  );
};