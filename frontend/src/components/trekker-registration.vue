<template>
  <div class="brand">
    <div>
        <h1>Treknologia</h1>
        <h4>Explore the unexplored</h4>
    </div>
  </div>
  <div class="registration-page">
    <div class="registration-card"; style="align-items: center;">
        <div class="form-section"; style="align-items: center;">
            <h1>Create User Account</h1>
            <p class="subtitle">Register as a Trekker</p>
            <form @submit.prevent="register">
                <div class="input-group">
                    <span>♙</span>
                    <input type="text" v-model="form.name" placeholder="Full Name" required/>
                </div>
                <div class="input-group">
                    <span>♙</span>
                    <input type="text" v-model="form.username" placeholder="Username" required/>
                </div>
                <div class="input-group">
                    <span>✉</span>
                    <input type="email" v-model="form.email" placeholder="Email address" required/>
                </div>
                <div class="input-group">
                    <span>♙</span>
                    <input type="password" v-model="form.password" placeholder="Password" required/>
                </div>
                <div class="input-group">
                    <span>♙</span>
                    <input type="password" v-model="form.confirmPassword" placeholder="Confirm Password" required/>
                </div>
                <div class="input-group">
                    <span>♧</span>
                    <input type="tel" v-model="form.contact" placeholder="Contact Number" required/>
                </div>
                <p v-if="error" class="error-message">{{ error }}</p>
                <button type="submit" class="register-button">Register</button>
            </form>
            <p class="login-link">Already have an account?<router-link to="/">Login here</router-link></p>
        </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "TrekkerRegistration",
  data() {
    return {form: {name: "", username: "", email: "", password: "", confirmPassword: "", contact: ""}, error: ""};
  },
  methods: {
    async register() {
      this.error = "";
      if (this.form.password !== this.form.confirmPassword) {
            this.error = "Passwords do not match.";
            return;
      }
      try {const res = await axios.post('http://127.0.0.1:5000/api/trekker/registration', this.form)
        alert('Registration successful!')
        this.$router.push('/')
      } catch (err) {
            console.log(err)
            console.log(err.response);
            if (err.response){
                alert(err.response.data.message)
            } else{
                alert("couldnt connect to server")
            }
      }
    }
  }
};
</script>

<style scoped>
* {box-sizing: border-box;}
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
.registration-page {
    width: 100%;
    min-height: 100vh;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-image: url("../assets/user-register.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    overflow-y: auto;
    padding: 20px;
    font-family: Arial, Helvetica, sans-serif;
}
.registration-card {
    width: 570px;
    max-width: 100%;
    padding: 25px 30px;
    border: 2px solid rgba(203, 213, 225, 0.9);
    border-radius: 12px;
    align-items: center;
    background: rgba(184, 214, 250, 0.9);
    backdrop-filter: blur(5px);
}
.form-section {
    width: 365px;
    max-width: 100%;
    margin-left: auto;
    margin-right: 65px;
}
.form-section h1 {
    margin: 0;
    text-align: center;
    font-size: 25px;
    font-weight: 700;
    color: #111827;
}
.subtitle {
    margin: 8px 0 20px;
    text-align: center;
    font-size: 16px;
    color: #111827;
}
.input-group {
    width: 100%;
    height: 44px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 11px;
    padding: 0 12px;
    border: 2px solid #dce3ec;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.95);
}
.input-group span {
    font-size: 19px;
    color: #52627a;
}
.input-group input {
    width: 100%;
    height: 100%;
    border: none;
    outline: none;
    background: transparent;
    font-size: 14px;
    color: #111827;
}
.input-group input::placeholder {color: #64748b;}
.input-group:focus-within {border-color: #155eef;}
.register-button {
    width: 100%;
    height: 43px;
    margin-top: 1px;
    border: none;
    border-radius: 6px;
    background: #155eef;
    color: white;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
}
.register-button:hover {background: #104bc4;}
.login-link {
    margin: 22px 0 15px;
    text-align: center;
    font-size: 14px;
    color: #111827;
}
.login-link a {
    margin-left: 4px;
    color: #075bea;
    font-weight: 700;
    text-decoration: none;
}
.login-link a:hover {text-decoration: underline;}
.note {
    width: 100%;
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-top: 20px;
    padding: 13px 15px;
    border: 2px solid #b7d0ff;
    border-radius: 8px;
    background: rgba(244, 247, 255, 0.85);
}
.note-icon {
    color: #155eef;
    font-size: 22px;
}
.note p {
    margin: 0;
    font-size: 14px;
    line-height: 1.7;
    color: #111827;
}
.error-message {
    margin: 8px 0;
    color: #dc2626;
    font-size: 13px;
}
@media (max-width: 700px) {
    .registration-page {padding: 15px;}
    .registration-card {padding: 25px 18px;}
    .form-section {width: 100%; margin: 0 auto;}
    .form-section h1 {font-size: 22px;}
    .note p {font-size: 12px;}
}
@media (max-height: 650px) {
    .registration-page {height: auto; min-height: 100vh;}
}
</style>