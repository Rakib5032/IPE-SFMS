import { useEffect } from "react";
import "./Toast.css";

export type ToastType =
  | "success"
  | "warning"
  | "error"
  | "info";

interface ToastProps {
  message: string;
  type?: ToastType;
  duration?: number;
  onClose: () => void;
}

function Toast({
  message,
  type = "info",
  duration,
  onClose,
}: ToastProps) {
  const toastDuration =
    duration ??
    (type === "success"
      ? 5000
      : type === "warning"
        ? 6000
        : type === "error"
          ? 8000
          : 5000);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      onClose();
    }, toastDuration);

    return () => {
      window.clearTimeout(timer);
    };
  }, [toastDuration, onClose]);

  const icon =
    type === "success"
      ? "✓"
      : type === "warning"
        ? "!"
        : type === "error"
          ? "×"
          : "i";

  const title =
    type === "success"
      ? "Success"
      : type === "warning"
        ? "Attention"
        : type === "error"
          ? "Error"
          : "Information";

  return (
    <div
      className={`toast toast-${type}`}
      role="alert"
      aria-live="polite"
    >
      <div className="toast-icon">
        {icon}
      </div>

      <div className="toast-content">
        <strong className="toast-title">
          {title}
        </strong>

        <span className="toast-message">
          {message}
        </span>
      </div>

      <button
        type="button"
        className="toast-close"
        onClick={onClose}
        aria-label="Close notification"
      >
        ×
      </button>

      <div
        className="toast-progress"
        style={{
          animationDuration: `${toastDuration}ms`,
        }}
      />
    </div>
  );
}

export default Toast;