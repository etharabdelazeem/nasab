<!--Login.vue -->
<template>
  <div class="login-page">
    <div class="logo-section">
      <img src="@/assets/logo.png" alt="Nasab Logo" class="logo" />
    </div>
    <div class="form-section">
      <form @submit.prevent="handleLogin" class="login-form">
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          class="input-field"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          class="input-field"
          required
        />
        <button type="submit" class="login-button">Log In</button>
      </form>
      <p class="signup-text">
        Don’t have an account yet? 
        <router-link to="/register" class="signup-link">Sign up!</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      // Add logic for login, e.g., API call
      console.log("Logging in with", this.email, this.password);
    },
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.logo-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo {
  width: 150px;
}

.form-section {
  flex: 1;
  width: 100%;
  max-width: 400px;
  padding: 0 20px;
  text-align: center;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.login-button {
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #333;
}

.signup-text {
  margin-top: 20px;
  color: #555;
}

.signup-link {
  color: #000;
  text-decoration: none;
  font-weight: bold;
}

.signup-link:hover {
  text-decoration: underline;
}
</style>

