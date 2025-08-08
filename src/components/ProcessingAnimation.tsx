import { useEffect, useState } from 'react';
import { FileText, Brain, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const ProcessingAnimation = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const navigate = useNavigate();

  const steps = [
    { icon: FileText, text: 'Reading PDF content...', duration: 2000 },
    { icon: Brain, text: 'Analyzing document structure...', duration: 2500 },
    { icon: CheckCircle, text: 'Generating summary...', duration: 2000 },
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      if (currentStep < steps.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        // Navigate to results after all steps
        setTimeout(() => {
          navigate('/result');
        }, 1500);
      }
    }, steps[currentStep].duration);

    return () => clearTimeout(timer);
  }, [currentStep, navigate, steps]);

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      {/* Background floating elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-primary/5 rounded-full animate-float" style={{ animationDelay: '0s' }} />
        <div className="absolute top-3/4 right-1/4 w-24 h-24 bg-accent/5 rounded-full animate-float" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/3 w-16 h-16 bg-primary-glow/5 rounded-full animate-float" style={{ animationDelay: '2s' }} />
      </div>

      <div className="glass-card p-12 text-center max-w-md w-full relative z-10">
        {/* Main processing animation */}
        <div className="mb-8">
          <div className="relative w-24 h-24 mx-auto mb-6">
            {/* Outer spinning ring */}
            <div className="absolute inset-0 border-4 border-primary/20 rounded-full processing-spin" />
            <div className="absolute inset-2 border-4 border-t-primary border-transparent rounded-full processing-spin" style={{ animationDirection: 'reverse' }} />
            
            {/* Center icon */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center processing-pulse">
                {(() => {
                  const CurrentIcon = steps[currentStep].icon;
                  return <CurrentIcon className="w-6 h-6 text-primary" />;
                })()}
              </div>
            </div>
          </div>
        </div>

        {/* Step text */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-foreground">
            Processing your PDF
          </h2>
          <p className="text-lg text-primary font-medium animate-fade-in" key={currentStep}>
            {steps[currentStep].text}
          </p>
        </div>

        {/* Progress indicators */}
        <div className="flex justify-center space-x-2 mt-8">
          {steps.map((_, index) => (
            <div
              key={index}
              className={`w-3 h-3 rounded-full transition-all duration-500 ${
                index <= currentStep 
                  ? 'bg-primary scale-110' 
                  : 'bg-muted'
              }`}
            />
          ))}
        </div>

        {/* Completion message */}
        {currentStep === steps.length - 1 && (
          <div className="mt-6 animate-fade-in">
            <p className="text-sm text-muted-foreground">
              Almost done! Preparing your results...
            </p>
          </div>
        )}
      </div>
    </div>
  );
};