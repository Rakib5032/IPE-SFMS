<template>
  <div class="login-wrapper">
    <div class="login-card" :class="{ 'shake-animation': shake }">
      <!-- Animated Avatar / Mascot Header -->
      <div class="mascot-container">
        <div class="mascot" :class="mascotState">
          <div class="eyes">
            <div class="eye left" :style="eyeFollowStyle"></div>
            <div class="eye right" :style="eyeFollowStyle"></div>
          </div>
          <div class="mouth"></div>
        </div>
      </div>

      <h2 class="title">Halt! Who goes there? 🧙‍♂️</h2>
      <p class="subtitle">{{ dynamicSubtitle }}</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>

          <div class="input-wrapper">
            <input
              id="username"
              v-model="username"
              type="text"
              required
              placeholder="e.g. MasterOfCode42"
              @focus="mascotState = 'watching'"
              @blur="mascotState = 'idle'"
              @mousemove="trackMouse"
            />
            <span class="focus-border"></span>
          </div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              required
              placeholder="Keep it secret, keep it safe..."
              @focus="mascotState = 'peeking'"
              @blur="mascotState = 'idle'"
            />
            <button
              type="button"
              class="toggle-pwd"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '🙈 Hide' : '👁️ Peek' }}
            </button>
          </div>
        </div>

        <!-- Funny Error Box -->
        <transition name="bounce">
          <div v-if="errorMessage" class="error-box">
            <span class="error-icon">💥</span>
            <span>{{ errorMessage }}</span>
          </div>
        </transition>

        <!-- Dynamic Action Button -->
        <button
          type="submit"
          class="submit-btn"
          :disabled="loading"
          :class="{ 'btn-loading': loading }"
        >
          <span v-if="!loading">Let Me In! 🚀</span>
          <span v-else class="spinner-text">Negotiating with server... 🍕</span>
        </button>
      </form>

      <div class="footer-joke">
        <p>Forgot password? Just try <code>123456</code> (Just kidding, please don't).</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const loading = ref(false);
const shake = ref(false);
const showPassword = ref(false);
const mascotState = ref('idle'); // idle, watching, peeking, shock, success

// Mouse tracking logic for eye movement
const mouseX = ref(0);
const mouseY = ref(0);

const trackMouse = (event) => {
  const rect = event.target.getBoundingClientRect();
  mouseX.value = (event.clientX - rect.left) / 10;
  mouseY.value = (event.clientY - rect.top) / 10;
};

const eyeFollowStyle = computed(() => {
  if (mascotState.value === 'watching') {
    return {
      transform: `translate(${Math.min(Math.max(mouseX.value, -6), 6)}px, ${Math.min(Math.max(mouseY.value, -4), 4)}px)`,
    };
  }
  return { transform: 'translate(0, 0)' };
});

const dynamicSubtitle = computed(() => {
  if (password.value.length > 0 && password.value.length < 4) {
    return "That's a bit short for a password, isn't it? 🤔";
  }
  if (password.value.length >= 12) {
    return "Whoa, Fort Knox in the house! 🏰";
  }
  return "Please identify yourself before entering the realm.";
});

const triggerShake = () => {
  shake.value = true;
  setTimeout(() => (shake.value = false), 600);
};

const funnyErrorResponses = [
  "Nice try, imposter! Wrong credentials. 🤖",
  "Hmm... The server says 'Nope!'. Check your spelling.",
  "Access denied! Did your cat step on the keyboard again?",
  "Wrong password! The guards have been alerted. 🚨",
];

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      const randomJoke = funnyErrorResponses[Math.floor(Math.random() * funnyErrorResponses.length)];
      throw new Error(data.detail ? `${data.detail} (${randomJoke})` : randomJoke);
    }

    const data = await response.json();
    
    mascotState.value = 'success';
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);

    setTimeout(() => {
      useRouter().push('/dashboard');
    }, 800);

  } catch (err) {
    mascotState.value = 'shock';
    errorMessage.value = err.message;
    triggerShake();
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Main Container Styling */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Poppins', sans-serif;
  padding: 20px;
}

.login-card {
  background: #ffffff;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 420px;
  text-align: center;
  position: relative;
  transition: transform 0.3s ease;
}

/* Header Text */
.title {
  margin: 10px 0 5px;
  color: #333;
  font-size: 1.6rem;
  font-weight: 700;
}

.subtitle {
  color: #666;
  font-size: 0.88rem;
  margin-bottom: 25px;
  min-height: 38px;
}

/* Mascot Head Animation */
.mascot-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.mascot {
  width: 80px;
  height: 80px;
  background: #ffbe0b;
  border-radius: 50%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: inset -4px -4px 0px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.eyes {
  display: flex;
  gap: 16px;
  position: absolute;
  top: 28px;
}

.eye {
  width: 12px;
  height: 12px;
  background: #222;
  border-radius: 50%;
  transition: transform 0.1s ease-out;
}

.mouth {
  width: 20px;
  height: 10px;
  border-bottom: 3px solid #222;
  border-radius: 0 0 10px 10px;
  position: absolute;
  bottom: 18px;
  transition: all 0.3s ease;
}

/* Mascot States */
.mascot.peeking .eye {
  height: 3px; /* Squint/Cover eyes */
  margin-top: 4px;
}

.mascot.shock {
  background: #ff0054;
}
.mascot.shock .mouth {
  height: 14px;
  width: 14px;
  border-radius: 50%;
  background: #222;
}

.mascot.success {
  background: #06d6a0;
  transform: scale(1.1);
}

/* Form Controls */
.form-group {
  text-align: left;
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 6px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  outline: none;
  font-size: 0.95rem;
  transition: border-color 0.2s ease;
}

input:focus {
  border-color: #667eea;
}

.toggle-pwd {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  font-size: 0.8rem;
  cursor: pointer;
  color: #666;
}

/* Funny Submit Button */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: all 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #5a67d8;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(102, 126, 234, 0.5);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

/* Error Banner & Animations */
.error-box {
  background: #fff5f5;
  border: 1px solid #feb2b2;
  color: #c53030;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.shake-animation {
  animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-2px, 0, 0); }
  20%, 80% { transform: translate3d(4px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-8px, 0, 0); }
  40%, 60% { transform: translate3d(8px, 0, 0); }
}

.bounce-enter-active {
  animation: bounce-in 0.3s;
}
.bounce-leave-active {
  animation: bounce-in 0.3s reverse;
}
@keyframes bounce-in {
  0% { transform: scale(0); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.footer-joke {
  margin-top: 25px;
  font-size: 0.75rem;
  color: #888;
}

code {
  background: #edf2f7;
  padding: 2px 6px;
  border-radius: 4px;
}
</style>