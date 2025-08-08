import React, { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import CompanyDetailsForm, { CompanyDetails } from '@/components/CompanyDetailsForm';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

const Upload = () => {
  const [currentStep, setCurrentStep] = useState<'company' | 'upload'>('company');
  const [companyDetails, setCompanyDetails] = useState<CompanyDetails | null>(null);

  const handleCompanyDetailsComplete = (details: CompanyDetails) => {
    setCompanyDetails(details);
    setCurrentStep('upload');
  };

  const handleBackToCompanyDetails = () => {
    setCurrentStep('company');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      {/* Background floating elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-primary/5 rounded-full animate-float" style={{ animationDelay: '0s' }} />
        <div className="absolute bottom-1/4 left-1/4 w-24 h-24 bg-accent/5 rounded-full animate-float" style={{ animationDelay: '1.5s' }} />
        <div className="absolute top-1/2 right-1/3 w-16 h-16 bg-primary-glow/5 rounded-full animate-float" style={{ animationDelay: '3s' }} />
      </div>

      <div className="w-full max-w-4xl mx-auto text-center relative z-10">
        {/* Header - shown on both steps */}
        <div className="mb-12 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            {currentStep === 'company' ? 'Company Information' : 'Upload Your'} 
            <span className="text-transparent bg-clip-text" style={{ backgroundImage: 'var(--gradient-primary)' }}>
              {currentStep === 'company' ? ' & Details' : ' PDF Files'}
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-lg mx-auto">
            {currentStep === 'company' 
              ? 'Enter your company details to start processing CERSAI reports'
              : 'Select PDF documents to generate comprehensive summary reports with intelligent analysis'
            }
          </p>
        </div>

        {/* Step Content */}
        <div className="animate-slide-up">
          {currentStep === 'company' ? (
            <CompanyDetailsForm onComplete={handleCompanyDetailsComplete} />
          ) : (
            <div className="space-y-6">
              {/* Back button and company details summary */}
              <div className="flex items-center justify-between mb-6 p-4 bg-muted/50 rounded-lg">
                <Button
                  variant="ghost"
                  onClick={handleBackToCompanyDetails}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Edit Company Details
                </Button>
                <div className="text-sm text-muted-foreground">
                  <span className="font-medium">{companyDetails?.companyName}</span>
                  {companyDetails?.cinNumber && (
                    <span className="ml-2">({companyDetails.cinNumber})</span>
                  )}
                </div>
              </div>
              
              <FileUpload companyDetails={companyDetails || undefined} />
            </div>
          )}
        </div>

        {/* Features highlight - only show on company step */}
        {currentStep === 'company' && (
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <div className="glass-card p-6 text-center">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-semibold text-foreground mb-2">Lightning Fast</h3>
              <p className="text-sm text-muted-foreground">Process documents in seconds with AI-powered analysis</p>
            </div>

            <div className="glass-card p-6 text-center">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="font-semibold text-foreground mb-2">Accurate Results</h3>
              <p className="text-sm text-muted-foreground">Advanced AI ensures precise content extraction</p>
            </div>

            <div className="glass-card p-6 text-center">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="font-semibold text-foreground mb-2">Secure Processing</h3>
              <p className="text-sm text-muted-foreground">Your documents are processed securely and privately</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload;