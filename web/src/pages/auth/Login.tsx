import React, { useEffect, useRef, useState } from "react";
import { login } from "../../services/authService";
import { setTokens } from "../../utils/storage";

import "./Login.css";

type MascotState =
  | "idle"
  | "watching"
  | "peeking"
  | "success";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [mascotState, setMascotState] =
    useState<MascotState>("idle");

  const [eyePos, setEyePos] = useState({
    x: 0,
    y: 0,
  });

  const [errorMessage, setErrorMessage] =
    useState("");

  const errorTimerRef =
    useRef<ReturnType<typeof setTimeout> | null>(null);

  /*
   * Track mouse position over Employee ID input
   * so the mascot eyes follow the cursor.
   */
  const trackMouse = (
    e: React.MouseEvent<HTMLInputElement>
  ) => {
    const rect =
      e.currentTarget.getBoundingClientRect();

    const x = Math.min(
      Math.max(
        (e.clientX - rect.left) / 10,
        -6
      ),
      6
    );

    const y = Math.min(
      Math.max(
        (e.clientY - rect.top) / 10,
        -4
      ),
      4
    );

    setEyePos({
      x,
      y,
    });
  };

  /*
   * Show login error.
   *
   * The warning stays visible for exactly 4 seconds.
   * If another error occurs before that, the previous
   * timer is cancelled and a new 4-second timer starts.
   */
  const showError = (message: string) => {
    /*
     * Clear the previous timer first.
     */
    if (errorTimerRef.current !== null) {
      clearTimeout(errorTimerRef.current);
      errorTimerRef.current = null;
    }

    /*
     * Show warning.
     */
    setErrorMessage(message);

    /*
     * Clear the form immediately after
     * the warning is triggered.
     */
    setUsername("");
    setPassword("");

    /*
     * Reset mascot.
     */
    setMascotState("idle");

    /*
     * Hide warning after exactly 4 seconds.
     */
    errorTimerRef.current = setTimeout(() => {
      setErrorMessage("");
      errorTimerRef.current = null;
    }, 4000);
  };

  /*
   * Cleanup timer when component unmounts.
   */
  useEffect(() => {
    return () => {
      if (errorTimerRef.current !== null) {
        clearTimeout(errorTimerRef.current);
        errorTimerRef.current = null;
      }
    };
  }, []);

  /*
   * Login handler
   */
  const handleLogin = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    /*
     * Stop an old warning timer when the user
     * starts another login attempt.
     */
    if (errorTimerRef.current !== null) {
      clearTimeout(errorTimerRef.current);
      errorTimerRef.current = null;
    }

    setErrorMessage("");

    /*
     * Employee ID validation
     */
    if (!username.trim()) {
      showError("Employee ID is required!");
      return;
    }

    /*
     * Password validation
     */
    if (!password) {
      showError("Password is required!");
      return;
    }

    try {
      setLoading(true);

      const tokens = await login({
        username: username.trim(),
        password,
      });

      /*
       * Successful login
       */
      setMascotState("success");

      setTokens(
        tokens.access_token,
        tokens.refresh_token
      );

      /*
       * Redirect to dashboard
       */
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 800);
    } catch (err: any) {
      console.error(
        "Login failed:",
        err
      );

      /*
       * Get API error message if available.
       */
      const apiErrorMessage =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Invalid Employee ID or Password!";

      /*
       * Show warning and clear form.
       */
      showError(
        typeof apiErrorMessage === "string"
          ? apiErrorMessage
          : "Invalid Employee ID or Password!"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">

      {/* =========================
          ERROR TOAST
          ========================= */}
      {errorMessage && (
        <div
          className="login-toast"
          role="alert"
          aria-live="assertive"
        >
          <div className="toast-emoji">
            😔
          </div>

          <div className="toast-content">
            <div className="toast-title">
              Login Failed
            </div>

            <div className="toast-message">
              {errorMessage}
            </div>
          </div>
        </div>
      )}

      {/* =========================
          LOGIN CARD
          ========================= */}
      <section className="login-card">

        {/* BRANDING HEADER */}
        <div className="branding-header">
          <div className="company-badge">
            FAKIR FASHION LTD.
          </div>

          <div className="dept-badge">
            IPE DEPARTMENT
          </div>
        </div>

        {/* MASCOT */}
        <div className="mascot-container">
          <div
            className={`mascot ${
              mascotState === "success"
                ? "mascot-success"
                : ""
            }`}
          >
            <div className="mascot-eyes">

              <div
                className="mascot-eye"
                style={{
                  transform:
                    mascotState === "watching"
                      ? `translate(${eyePos.x}px, ${eyePos.y}px)`
                      : "none",

                  height:
                    mascotState === "peeking"
                      ? "3px"
                      : "12px",
                }}
              />

              <div
                className="mascot-eye"
                style={{
                  transform:
                    mascotState === "watching"
                      ? `translate(${eyePos.x}px, ${eyePos.y}px)`
                      : "none",

                  height:
                    mascotState === "peeking"
                      ? "3px"
                      : "12px",
                }}
              />

            </div>

            <div className="mascot-mouth" />
          </div>
        </div>

        {/* TITLE */}
        <h1 className="login-title">
          Halt! Who goes there? 🧙‍♂️
        </h1>

        <p className="login-subtitle">
          Please identify yourself before entering.
        </p>

        {/* LOGIN FORM */}
        <form
          className="login-form"
          onSubmit={handleLogin}
          noValidate
        >

          {/* EMPLOYEE ID */}
          <div className="form-group">
            <label
              className="form-label"
              htmlFor="username"
            >
              Employee ID
            </label>

            <input
              id="username"
              type="text"
              inputMode="numeric"
              required
              placeholder="e.g. 10024"
              value={username}
              onChange={(e) =>
                setUsername(e.target.value)
              }
              onFocus={() =>
                setMascotState("watching")
              }
              onBlur={() =>
                setMascotState("idle")
              }
              onMouseMove={trackMouse}
              className="form-input"
              autoComplete="username"
              disabled={loading}
            />
          </div>

          {/* PASSWORD */}
          <div className="form-group">
            <label
              className="form-label"
              htmlFor="password"
            >
              Password
            </label>

            <div className="input-wrapper">

              <input
                id="password"
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                required
                placeholder="Keep it secret, keep it safe..."
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                onFocus={() =>
                  setMascotState("peeking")
                }
                onBlur={() =>
                  setMascotState("idle")
                }
                className="form-input"
                autoComplete="current-password"
                disabled={loading}
              />

              <button
                type="button"
                onClick={() =>
                  setShowPassword(
                    !showPassword
                  )
                }
                className="toggle-btn"
                tabIndex={-1}
                disabled={loading}
              >
                {showPassword
                  ? "🙈 Hide"
                  : "👁️ Peek"}
              </button>

            </div>
          </div>

          {/* SUBMIT BUTTON */}
          <button
            type="submit"
            disabled={loading}
            className="submit-btn"
          >
            {loading
              ? "Checking details... 🍕"
              : "Let Me In! 🚀"}
          </button>

        </form>

        {/* FOOTER */}
        <div className="footer-branding">
          <span>
            FAKIR FASHION LTD.
          </span>

          <span>
            IPE DEPARTMENT
          </span>
        </div>

      </section>
    </main>
  );
}