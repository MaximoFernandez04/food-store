import { type InputHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const inputId = id ?? props.name;
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label htmlFor={inputId} className="text-sm font-medium text-ink-soft">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={clsx(
            "rounded-lg border bg-surface px-3.5 py-2.5 text-sm text-ink placeholder:text-ink-soft/60",
            "transition-colors focus:outline-none",
            error ? "border-brasa-500" : "border-line focus:border-mostaza-500",
            className
          )}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : undefined}
          {...props}
        />
        {error && (
          <p id={`${inputId}-error`} className="text-sm text-brasa-500">
            {error}
          </p>
        )}
      </div>
    );
  }
);
Input.displayName = "Input";
