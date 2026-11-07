<template>
  <div class="trekking-login">
    <div class="login-card">
      <div class="left-panel">
        <div class="brand">
          <div>
                <h1>Treknologia</h1>
                <h4>Explore the unexplored</h4>
            </div>
        </div>

        <div class="roles-section">
          <h2>ROLES</h2>

          <div class="roles-list">
            <div class="role-item" :class="{ active: selectedRole === 'Admin' }" @click="selectRole('Admin')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 20V10l5 3 3-8 3 8 5-3v10H4Z" />
                <path d="M12 5V2m-2 2 2 2 2-2" />
              </svg>
              <span>Admin</span>
            </div>

            <div class="role-item" :class="{ active: selectedRole === 'Staff' }" @click="selectRole('Staff')">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <circle cx="12" cy="7" r="4" />
                <path d="M4 21v-2a8 8 0 0 1 16 0v2H4Z" />
              </svg>
              <span>Staff</span>
            </div>

            <div class="role-item" :class="{ active: selectedRole === 'Trekker' }" @click="selectRole('Trekker')">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <circle cx="13" cy="4" r="2.5" />
                <path d="m11 8 4 2 3 4-2 1-3-3-2 4 3 5h-3l-3-5-2 4H3l4-8 1-4 3 1Z" />
                <path d="m15 8 4 2 2 4-2 1-2-3" />
              </svg>
              <span>Trekker</span>
            </div>
          </div>
        </div>
      </div>

      <div class="right-panel">
        <div class="login-heading">
            <h2>{{ selectedRole }} Login</h2>
            <p>Login to your {{ selectedRole.toLowerCase() }} account</p>
        </div>

        <form @submit.prevent="login">
          <label class="input-field">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="8" r="4" />
              <path d="M5 21v-2a7 7 0 0 1 14 0v2H5Z" />
            </svg>
            <input v-model="username" type="text" placeholder="Username" required />
          </label>

          <label class="input-field">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="4" y="10" width="16" height="11" rx="2" />
              <path d="M8 10V7a4 4 0 0 1 8 0v3" />
              <circle cx="12" cy="15" r="1" />
              <path d="M12 16v2" />
            </svg>
            <input v-model="password" type="password" placeholder="Password" required />
          </label>

          <label class="remember">
            <input v-model="rememberMe" type="checkbox" />
            <span>Remember me</span>
          </label>

          <button class="login-button" type="submit">Login</button>

          <div class="register-section">
            <p>Don't have an account?</p>
            <button type="button" class="register-link" @click="register">
              Register as User (Trekker)
            </button>
          </div>
        </form>
      </div>

      <div class="notice">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="9" />
          <path d="M12 11v5m0-8h.01" />
        </svg>

        <p>
          <strong>Note:</strong> Only Users (Trekkers) can register themselves.
          Trekking Staff are created by Admin.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LoginPage",

  data() {
    return {
      username: "",
      password: "",
      rememberMe: false,
      selectedRole: "Admin"
    };
  },

  methods: {
    selectRole(role) {
      this.selectedRole = role;
      this.username = "";
      this.password = "";
      this.rememberMe = false;
    },
    async login() {
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/api/login",
                {
                    username: this.username,
                    password: this.password,
                    role: this.selectedRole
                }
            );

            if (response.data.success) {
                
                if (response.data.role === "Admin") {
                    localStorage.setItem("token", response.data.token);
                    alert('Login successful!')
                    this.$emit('logged-in')
                    this.$router.push("/admin/dashboard");
                } else if (response.data.role === "Staff") {
                    localStorage.setItem("token", response.data.token);
                    alert('Login successful!')
                    this.$emit('logged-in')
                    this.$router.push("/staff/dashboard");
                } else if (response.data.role === "Trekker") {
                    localStorage.setItem("token", response.data.token);
                    alert('Login successful!')
                    this.$emit('logged-in')
                    this.$router.push("/trekker/dashboard");
                }
            }
        } catch (error) {
            alert(
                error.response?.data?.message ||
                "Login failed. Please check your credentials."
            );
        }
    },

    register() {
      this.$router.push("/trekker/registration");
    }
  }
};
</script>

<style scoped>
* {
    box-sizing: border-box;
}

.trekking-login {
    width: 100%;
    height: 100vh;
    min-height: 100vh;
    display: flex;
    align-items: stretch;
    justify-content: center;
    padding: 0;
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    color: #111827;
    background-image: url("../assets/trekking.jpg");
    background-position: center center;
    background-size: cover;
    background-repeat: no-repeat;
    overflow: hidden;
    position: relative;
}

.login-card {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100vh;
    min-height: 0;
    padding: 28px 32px 24px;
    display: grid;
    grid-template-columns: 1fr 1.12fr;
    grid-template-rows: 1fr auto;
    column-gap: 32px;
    row-gap: 22px;
    background: transparent;
    border: none;
    border-radius: 0;
    box-shadow: none;
}

:global(html),
:global(body),
:global(#app) {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}

:global(body) {
    overflow: hidden;
}

.left-panel {
    position: static;
    min-width: 0;
    padding-top: 4px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.brand {
    position: absolute;
    top: 0;
    left: -32px;
    right: -32px;
    display: flex;
    align-items: center;
    justify-content: left;
    padding: 5px 30px;
    background: rgba(184, 214, 250, 0.9);
    border-bottom: 1px solid rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(2px);
    z-index: 5;
}

.brand h1 {
    margin: 0;
    font-size: 30px;
    padding: 0px 30px;
    font-weight: bold;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    color: #00027f;
    text-align: left;
}
.brand h4 {
    margin: 0;
    font-size: 15px;
    padding: 0px 35px;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
    font-style: italic;
    color: #00027f;
    text-align: left;
}

.roles-section {
    position: relative;
    z-index: 2;
    margin-top: 250px;
    margin-left: 85px;
    width: 492px;
    max-width: 100%;
    padding: 12px;
    border-radius: 10px;
    background: rgba(184, 214, 250, 0.9);
    backdrop-filter: blur(3px);
}

.roles-section h2 {
    margin: 0 0 14px 3px;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.roles-list {
    width: 100%;
    border: 1.5px solid rgba(203, 213, 225, 0.95);
    border-radius: 9px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.92);
}

.role-item {
    display: flex;
    align-items: center;
    gap: 16px;
    height: 64px;
    padding: 0 18px;
    border-bottom: 1.5px solid #cbd5e1;
    font-size: 24px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease, color 0.2s ease;
}

.role-item:hover {
    background: rgba(21, 94, 239, 0.10);
}

.role-item.active {
    background: rgba(21, 94, 239, 0.15);
    color: #155eef;
    border-left: 4px solid #155eef;
}

.role-item.active svg {
    color: #155eef;
}

.role-item:last-child {
    border-bottom: none;
}

.role-item svg {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
}

.right-panel {
    align-self: center;
    position: relative;
    margin-top: 150px;
    z-index: 3;
    min-width: 0;
    width: 100%;
    max-width: 560px;
    justify-self: center;
    padding: 30px 28px 24px;
    border: 2px solid rgba(212, 219, 229, 0.95);
    border-radius: 13px;
    background: rgba(184, 214, 250, 0.9);
    box-shadow: 0 8px 28px rgba(15, 23, 42, 0.12);
    backdrop-filter: blur(4px);
}

.login-heading {
    text-align: center;
    margin-bottom: 26px;
}

.login-heading h2 {
    margin: 0 0 7px;
    font-size: 22px;
    line-height: 1.2;
    font-weight: 700;
}

.login-heading p {
    margin: 0;
    font-size: 14px;
    color: #374151;
}

.input-field {
    height: 48px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 13px;
    margin-bottom: 15px;
    border: 1.5px solid #d5dce5;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.96);
}

.input-field svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
    color: #475569;
}

.input-field input {
    width: 100%;
    min-width: 0;
    border: none;
    outline: none;
    background: transparent;
    font-family: inherit;
    font-size: 13px;
    color: #111827;
}

.input-field input::placeholder {
    color: #64748b;
    opacity: 1;
}

.remember {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 5px 0 20px;
    font-size: 13px;
    cursor: pointer;
}

.remember input {
    width: 16px;
    height: 16px;
    margin: 0;
    accent-color: #155eef;
}

.login-button {
    width: 100%;
    height: 47px;
    border: none;
    border-radius: 5px;
    background: #155eef;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
}

.login-button:hover {
    background: #104bc4;
}

.register-section {
    margin-top: 27px;
    text-align: center;
}

.register-section p {
    margin: 0 0 12px;
    font-size: 13px;
    color: #111827;
}

.register-link {
    padding: 0;
    border: none;
    background: transparent;
    color: #155eef;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
}

.register-link:hover {
    text-decoration: underline;
}

.notice {
    grid-column: 1 / -1;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px 20px;
    background: rgba(244, 247, 255, 0.0);
    color: #e6e8ee;
    backdrop-filter: blur(2px);
}

.notice svg {
    width: 21px;
    height: 21px;
    flex-shrink: 0;
    color: #155eef;
    margin-top: 1px;
}

.notice p {
    margin: 0;
    font-size: 13px;
    line-height: 1.65;
}

.notice strong {
    font-weight: 700;
}

@media (max-width: 760px) {
    .trekking-login {
        background-attachment: scroll;
        overflow: auto;
        height: auto;
    }

    .login-card {
        min-height: 100vh;
        height: auto;
        padding: 90px 16px 20px;
        grid-template-columns: 1fr;
        grid-template-rows: auto auto auto;
        gap: 22px;
    }

    .brand {
        left: -16px;
        right: -16px;
        padding: 12px 10px;
    }

    .brand h1 {
        font-size: 19px;
    }

    .left-panel {
        min-height: auto;
    }

    .roles-section {
        margin-top: 24px;
        width: 100%;
    }

    .role-item {
        height: 48px;
    }

    .right-panel {
        align-self: auto;
        padding: 25px 20px;
    }

    .notice {
        grid-column: 1;
        padding: 13px;
    }
}

@media (max-width: 380px) {
    .login-card {
        padding: 80px 14px 14px;
    }

    .right-panel {
        padding: 22px 15px;
    }

    .brand h1 {
        font-size: 17px;
    }

    .notice p {
        font-size: 12px;
    }
}
</style>