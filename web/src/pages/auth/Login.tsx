import { useState } from "react";
import type { FormEvent } from "react";
import { login } from "../../services/authService";
import { setTokens } from "../../utils/storage";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");

    if (!username.trim()) {
      setError("Employee ID is required");
      return;
    }

    if (!password) {
      setError("Password is required");
      return;
    }

    try {
      setLoading(true);

      const tokens = await login({
        username: username.trim(),
        password,
      });

      setTokens(
        tokens.access_token,
        tokens.refresh_token
      );

      window.location.href = "/dashboard";
    } catch {
      setError(
        "Invalid Employee ID or password"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-header">
          <h1>SFMS</h1>
          <p>
            Sewing Floor Management System
          </p>
        </div>

        <form
          className="login-form"
          onSubmit={handleSubmit}
        >
          <div className="form-group">
            <label htmlFor="username">
              Employee ID
            </label>

            <input
              id="username"
              type="text"
              inputMode="numeric"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              placeholder="Enter Employee ID"
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter password"
              autoComplete="current-password"
            />
          </div>

          {error && (
            <div className="login-error">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign In"}
          </button>
        </form>
      </section>
    </main>
  );
}

export default Login;