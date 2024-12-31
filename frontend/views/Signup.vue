<!--Signup.vue-->
<template>
  <div class="signup-page">
    <div class="logo-section">
      <img src="@/assets/logo.png" alt="Nasab Logo" class="logo" />
    </div>
    <div class="form-section">
      <form @submit.prevent="handleSignup" class="signup-form">
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
        <input
          type="password"
          v-model="confirmPassword"
          placeholder="Confirm Password"
          class="input-field"
          required
        />
        <button type="submit" class="signup-button">Sign Up</button>
      </form>
      <p class="login-text">
        Already have an account? 
        <router-link to="/login" class="login-link">Log in!</router-link>
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
      confirmPassword: "",
    };
  },
  methods: {
    handleSignup() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      // Add logic for signup, e.g., API call
      console.log("Signing up with", this.email, this.password);
    },
  },
};
</script>

<style scoped>
.signup-page {
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

.signup-button {
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

.signup-button:hover {
  background-color: #333;
}

.login-text {
  margin-top: 20px;
  color: #555;
}

.login-link {
  color: #000;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}
</style>

