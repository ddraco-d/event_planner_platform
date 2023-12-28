<template>
  <div class="home">
    <div class="welcome-message">
      <h1>Добро пожаловать в Event Planner Platform!</h1>
      <p>Выберите что вы хотите сделать</p>
      <nav class="navigation">
        <ul>
          <li><router-link to="/login" class="nav-item">Вход</router-link></li>
          <li><router-link to="/register" class="nav-item">Регистрация</router-link></li>
          <li><router-link to="/eventlist" class="nav-item">Список событий</router-link></li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.welcome-message {
  text-align: center;
  color: white;
  padding: 20px;
  border-radius: 15px;
  background: rgba(0, 0, 0, 0.5); /* Добавляем полупрозрачный фон вокруг текста и кнопок */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.welcome-message h1 {
  font-size: 2.5em;
  margin-bottom: 0.5em;
}

.welcome-message p {
  font-size: 1.2em;
  margin-bottom: 2em;
}

.navigation ul {
  list-style-type: none;
  padding: 0;
}

.navigation li {
  display: inline-block;
  margin: 0 10px;
}

.nav-item {
  text-decoration: none;
  color: #ffffff;
  font-size: 1.1em;
  padding: 10px 20px;
  border: 2px solid #ffffff;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.nav-item:hover,
.nav-item:focus {
  color: #000;
  background-color: #ffffff;
}
</style>