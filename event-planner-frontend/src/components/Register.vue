<template>
  <div class="login-container">
    <h1>Register</h1>
    <form @submit.prevent="register" class="login-form">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit" class="login-button">Register</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage', // Изменили на многословное имя
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    async register() {
      try {
        await this.$http.post('/users/', {
          username: this.username,
          password: this.password,
        });
        this.$router.push('/login');
      } catch (error) {
        alert('Возможно, такой пользователь уже существует');
        console.error('Ошибка регистрации:', error);
      }
    },
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

/* Дополнительные стили для инпутов */
input {
  margin-bottom: 10px;
  padding: 10px;
  padding-right: 15px; /* Добавлен отступ справа для внутреннего содержимого */
  border-radius: 5px;
  border: 1px solid #ddd;
  width: calc(100% - 15px); /* Уменьшаем ширину на величину отступа */
  box-sizing: border-box; /* Убедитесь, что padding включен в ширину */
}
</style>