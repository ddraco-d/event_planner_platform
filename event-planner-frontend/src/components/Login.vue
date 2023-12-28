<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="login" class="login-form">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit" class="login-button">Login</button>
    </form>
    <div class="register-prompt">
      <p>Нет аккаунта?</p>
      <button @click="goToRegister" class="register-button">Зарегистрироваться</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage', // Изменили на многословное имя
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);

      try {
        const response = await this.$http.post('/token', formData);
        // Сохраните токен в localStorage и обновите состояние Vuex
        const token = response.data.access_token;
        const role = response.data.role;
        const exp = response.data.exp;
        localStorage.setItem('access_token', token);
        localStorage.setItem('token_expires_at', exp);
        localStorage.setItem('role', role);
        this.$store.commit('setAccessToken', token);
        this.$store.commit('setUserRole', role);
        await this.$router.push('/eventlist');
      } catch (error) {
        alert('Неправильное имя пользователя или пароль');
        console.error('Ошибка входа:', error);
      }
    },
    goToRegister() {
      this.$router.push('/register'); // Измените на ваш путь регистрации
    }
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-form {
  background: rgba(0, 0, 0, 0.5);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.login-button {
  text-decoration: none;
  color: #ffffff;
  font-size: 1.1em;
  padding: 10px 20px;
  border: 2px solid #ffffff;
  border-radius: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
  background: transparent;
  outline: none;
}

.login-button:hover,
.login-button:focus {
  color: #000;
  background-color: #ffffff;
}

/* Дополнительные стили для инпутов, если нужно */
input {
  margin-bottom: 10px;
  padding: 10px;
  padding-right: 15px; /* Добавлен отступ справа для внутреннего содержимого */
  border-radius: 5px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box; /* Убедитесь, что padding включен в ширину */
}

.register-prompt {
  text-align: center;
  margin-top: 20px;
}

.register-button {
  text-decoration: none;
  color: #ffffff;
  font-size: 1em;
  padding: 10px 20px;
  border: 2px solid #ffffff;
  border-radius: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
  background: transparent;
  outline: none;
}

.register-button:hover,
.register-button:focus {
  color: #000;
  background-color: #ffffff;
}

</style>