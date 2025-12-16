<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-left">
        <h2>Advisor Portal</h2>
        <p>Sign in to manage your profile and keep your advisor details up to date.</p>
        <ul>
          <li>Real API: POST /auth/login/</li>
          <li>We store access/refresh tokens locally</li>
          <li>Redirects to your profile after login</li>
        </ul>
      </div>
      <div class="login-right">
        <el-card shadow="hover">
          <div class="login-form__header">
            <div>
              <p class="eyebrow">Secure access</p>
              <h3>Log in</h3>
            </div>
            <el-tag type="success">Live API</el-tag>
          </div>
          <form @submit.prevent="handleSubmit">
            <base-input
              v-model="form.username"
              label="Username or Email"
              placeholder="Enter username"
              :error="errors.username"
              clearable
              autocomplete="username"
            />
            <base-input
              v-model="form.password"
              label="Password"
              type="password"
              placeholder="Enter password"
              :error="errors.password"
              show-password
              autocomplete="current-password"
            />
            <el-button
              type="primary"
              native-type="submit"
              :loading="loading"
              class="login-button"
              block
            >
              Log in
            </el-button>
          </form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import BaseInput from '../components/BaseInput.vue';
import { login } from '../services/auth';

export default {
  name: 'Login',
  components: { BaseInput },
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      errors: {},
      loading: false
    };
  },
  methods: {
    validate() {
      const errors = {};
      if (!this.form.username) {
        errors.username = 'Username or email is required.';
      }
      if (!this.form.password) {
        errors.password = 'Password is required.';
      }
      this.errors = errors;
      return Object.keys(errors).length === 0;
    },
    async handleSubmit() {
      if (!this.validate()) return;
      this.loading = true;
      try {
        await login(this.form);
        this.$message.success('登录成功');
        this.$router.push('/profile');
      } catch (error) {
        const msg = error?.response?.data?.detail || error.message || 'Login failed';
        this.$message.error(msg);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 100%;
  max-width: 1000px;
  background: #fff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 20px 60px rgba(50, 91, 194, 0.08);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  align-items: stretch;
}

.login-left {
  background: linear-gradient(160deg, #1f8efa 0%, #7fc4ff 80%);
  color: #fff;
  border-radius: 14px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 0 15px 35px rgba(0, 72, 169, 0.25);
}

.login-left h2 {
  margin: 0;
  font-size: 26px;
}

.login-left p {
  margin: 4px 0 10px;
  opacity: 0.9;
}

.login-left ul {
  padding-left: 18px;
  margin: 0;
  display: grid;
  gap: 8px;
  font-size: 14px;
  opacity: 0.95;
}

.login-right {
  padding: 6px;
}

.login-form__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 11px;
  color: #7a8499;
}

.login-form__header h3 {
  margin: 4px 0 0;
}

.login-form__hint {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 0 10px;
  color: #7a8499;
  font-size: 13px;
}

.login-button {
  margin-top: 6px;
}

@media (max-width: 640px) {
  .login-card {
    padding: 20px;
  }

  .login-left {
    order: 2;
  }

  .login-right {
    order: 1;
  }
}
</style>
