import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { ChevronRight, Building2 } from 'lucide-react';

export interface CompanyDetails {
  companyName: string;
  cinNumber: string;
  searchReferenceId: string;
  dateOfIncorporation: string;
  udin: string;
  registeredOffice: string;
}

interface CompanyDetailsFormProps {
  onComplete: (details: CompanyDetails) => void;
}

interface ValidationErrors {
  companyName?: string;
  cinNumber?: string;
  searchReferenceId?: string;
  dateOfIncorporation?: string;
  udin?: string;
  registeredOffice?: string;
}

const CompanyDetailsForm: React.FC<CompanyDetailsFormProps> = ({ onComplete }) => {
  const [formData, setFormData] = useState<CompanyDetails>({
    companyName: '',
    cinNumber: '',
    searchReferenceId: '',
    dateOfIncorporation: '',
    udin: '',
    registeredOffice: ''
  });

  const [errors, setErrors] = useState<ValidationErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateField = (name: string, value: string): string | undefined => {
    switch (name) {
      case 'companyName':
        return !value.trim() ? 'Company name is required' : undefined;
      
      case 'cinNumber':
        if (!value.trim()) return 'CIN number is required';
        if (value.length > 25) return 'CIN number must be ≤25 characters';
        if (!/^[A-Z0-9]+$/.test(value)) return 'CIN must contain only uppercase letters and digits';
        return undefined;
      
      case 'searchReferenceId':
        if (!value.trim()) return 'Search Reference ID is required';
        if (value.length > 15) return 'Search Reference ID must be ≤15 digits';
        if (!/^\d+$/.test(value)) return 'Search Reference ID must contain only numbers';
        return undefined;
      
      case 'dateOfIncorporation':
        if (!value.trim()) return 'Date of incorporation is required';
        if (!/^\d{2}\.\d{2}\.\d{4}$/.test(value)) return 'Date must follow DD.MM.YYYY format';
        // Additional date validation
        const [day, month, year] = value.split('.').map(Number);
        const date = new Date(year, month - 1, day);
        if (date.getDate() !== day || date.getMonth() !== month - 1 || date.getFullYear() !== year) {
          return 'Please enter a valid date';
        }
        return undefined;
      
      case 'udin':
        if (!value.trim()) return 'UDIN is required';
        if (value.length > 20) return 'UDIN must be ≤20 characters';
        if (!/^[A-Z0-9]+$/.test(value)) return 'UDIN must contain only uppercase letters and digits';
        return undefined;
      
      case 'registeredOffice':
        return !value.trim() ? 'Registered office address is required' : undefined;
      
      default:
        return undefined;
    }
  };

  const handleInputChange = (name: string, value: string) => {
    // Apply transformations based on field type
    let transformedValue = value;
    
    if (name === 'cinNumber' || name === 'udin') {
      transformedValue = value.toUpperCase();
    } else if (name === 'searchReferenceId') {
      transformedValue = value.replace(/\D/g, ''); // Only digits
    } else if (name === 'dateOfIncorporation') {
      // Auto-format date as user types
      const digitsOnly = value.replace(/\D/g, '');
      if (digitsOnly.length <= 2) {
        transformedValue = digitsOnly;
      } else if (digitsOnly.length <= 4) {
        transformedValue = digitsOnly.slice(0, 2) + '.' + digitsOnly.slice(2);
      } else if (digitsOnly.length <= 8) {
        transformedValue = digitsOnly.slice(0, 2) + '.' + digitsOnly.slice(2, 4) + '.' + digitsOnly.slice(4);
      }
    }

    setFormData(prev => ({ ...prev, [name]: transformedValue }));
    
    // Clear error when user starts typing
    if (errors[name as keyof ValidationErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: ValidationErrors = {};
    
    Object.entries(formData).forEach(([key, value]) => {
      const error = validateField(key, value);
      if (error) {
        newErrors[key as keyof ValidationErrors] = error;
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    // Simulate a brief delay for better UX
    await new Promise(resolve => setTimeout(resolve, 500));
    
    onComplete(formData);
    setIsSubmitting(false);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="mb-8 text-center">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <Building2 className="w-8 h-8 text-primary" />
        </div>
        <h2 className="text-2xl font-bold text-foreground mb-2">Company Details</h2>
        <p className="text-muted-foreground">Please fill in the company information before uploading PDF files</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Company Name */}
          <div className="md:col-span-2">
            <Label htmlFor="companyName" className="text-sm font-medium">
              Name of the Company <span className="text-destructive">*</span>
            </Label>
            <Input
              id="companyName"
              type="text"
              value={formData.companyName}
              onChange={(e) => handleInputChange('companyName', e.target.value)}
              placeholder="Enter company name"
              className={`mt-1 ${errors.companyName ? 'border-destructive' : ''}`}
            />
            {errors.companyName && (
              <p className="text-sm text-destructive mt-1">{errors.companyName}</p>
            )}
          </div>

          {/* CIN Number */}
          <div>
            <Label htmlFor="cinNumber" className="text-sm font-medium">
              CIN Number <span className="text-destructive">*</span>
            </Label>
            <Input
              id="cinNumber"
              type="text"
              value={formData.cinNumber}
              onChange={(e) => handleInputChange('cinNumber', e.target.value)}
              placeholder="U12345AB1234PTC567890"
              maxLength={25}
              className={`mt-1 ${errors.cinNumber ? 'border-destructive' : ''}`}
            />
            <p className="text-xs text-muted-foreground mt-1">Max 25 characters, uppercase letters and digits only</p>
            {errors.cinNumber && (
              <p className="text-sm text-destructive mt-1">{errors.cinNumber}</p>
            )}
          </div>

          {/* Search Reference ID */}
          <div>
            <Label htmlFor="searchReferenceId" className="text-sm font-medium">
              Search Reference ID <span className="text-destructive">*</span>
            </Label>
            <Input
              id="searchReferenceId"
              type="text"
              value={formData.searchReferenceId}
              onChange={(e) => handleInputChange('searchReferenceId', e.target.value)}
              placeholder="123456789012345"
              maxLength={15}
              className={`mt-1 ${errors.searchReferenceId ? 'border-destructive' : ''}`}
            />
            <p className="text-xs text-muted-foreground mt-1">Max 15 digits, numbers only</p>
            {errors.searchReferenceId && (
              <p className="text-sm text-destructive mt-1">{errors.searchReferenceId}</p>
            )}
          </div>

          {/* Date of Incorporation */}
          <div>
            <Label htmlFor="dateOfIncorporation" className="text-sm font-medium">
              Date of Incorporation <span className="text-destructive">*</span>
            </Label>
            <Input
              id="dateOfIncorporation"
              type="text"
              value={formData.dateOfIncorporation}
              onChange={(e) => handleInputChange('dateOfIncorporation', e.target.value)}
              placeholder="DD.MM.YYYY"
              maxLength={10}
              className={`mt-1 ${errors.dateOfIncorporation ? 'border-destructive' : ''}`}
            />
            <p className="text-xs text-muted-foreground mt-1">Format: DD.MM.YYYY</p>
            {errors.dateOfIncorporation && (
              <p className="text-sm text-destructive mt-1">{errors.dateOfIncorporation}</p>
            )}
          </div>

          {/* UDIN */}
          <div>
            <Label htmlFor="udin" className="text-sm font-medium">
              UDIN <span className="text-destructive">*</span>
            </Label>
            <Input
              id="udin"
              type="text"
              value={formData.udin}
              onChange={(e) => handleInputChange('udin', e.target.value)}
              placeholder="12345ABCDE67890FGHIJ"
              maxLength={20}
              className={`mt-1 ${errors.udin ? 'border-destructive' : ''}`}
            />
            <p className="text-xs text-muted-foreground mt-1">Max 20 characters, uppercase letters and digits only</p>
            {errors.udin && (
              <p className="text-sm text-destructive mt-1">{errors.udin}</p>
            )}
          </div>

          {/* Registered Office */}
          <div className="md:col-span-2">
            <Label htmlFor="registeredOffice" className="text-sm font-medium">
              Registered Office <span className="text-destructive">*</span>
            </Label>
            <Textarea
              id="registeredOffice"
              value={formData.registeredOffice}
              onChange={(e) => handleInputChange('registeredOffice', e.target.value)}
              placeholder="Enter complete registered office address"
              rows={3}
              className={`mt-1 ${errors.registeredOffice ? 'border-destructive' : ''}`}
            />
            {errors.registeredOffice && (
              <p className="text-sm text-destructive mt-1">{errors.registeredOffice}</p>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center pt-4">
          <Button
            type="submit"
            disabled={isSubmitting}
            className="px-8 py-3 h-12 text-lg font-medium"
          >
            {isSubmitting ? (
              'Validating...'
            ) : (
              <>
                Next
                <ChevronRight className="w-5 h-5 ml-2" />
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default CompanyDetailsForm;
