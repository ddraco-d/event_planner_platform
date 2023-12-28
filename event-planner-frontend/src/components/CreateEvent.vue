<template>
  <div>
    <!-- Название платформы с ссылкой -->
    <div class="header">
      <router-link to="/eventlist" class="brand">EventPlatform</router-link>
      <div>
        <!-- Первая группа кнопок -->
        <div>
          <router-link to="/login" class="login-button">Login</router-link>
          <router-link to="/register" class="register-button">Register</router-link>
        </div>
        <!-- Вторая группа кнопок -->
        <div>
          <!-- Используйте router-link вместо button для "Добавить событие" -->
          <router-link
              v-if="userHasRole('organizer') || userHasRole('admin')"
              to="/createevent"
              class="admin-button"
          >
            Добавить событие
          </router-link>

          <!-- Используйте router-link вместо button для "Администрирование" -->
          <router-link
              v-if="userHasRole('admin')"
              to="/eventadmin"
              class="admin-button"
          >
            Администрирование
          </router-link>
        </div>
      </div>
    </div>


    <div class="container">
      <!-- Код пропущен для краткости -->
      <h1>Создать событие</h1>
      <form @submit.prevent="createEvent" class="event-form">
        <div class="form-group">
          <input type="text" v-model="event.title" placeholder="Название события" required class="input-style">
        </div>
        <div class="form-group">
          <textarea v-model="event.description" placeholder="Описание события" required class="input-style"></textarea>
        </div>
        <div class="form-group">
          <input type="date" v-model="event.date" required class="input-style">
        </div>
        <div class="form-group">
          <button type="submit" class="create-button">Создать</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      event: {
        title: '',
        description: '',
        date: '' // Инициализируйте свойство для даты
      }
    };
  },
  methods: {
    async createEvent() {
      if (!this.userHasRole('organizer') && !this.userHasRole('admin')) {
        alert('Только организаторы или администраторы могут создавать события.');
        return;
      }
      try {
        await this.$http.post('/create_event', this.event);
        alert('Событие успешно создано!');
        // Переход к списку событий или к деталям созданного события
      } catch (error) {
        console.error("Ошибка при создании события:", error);
      }
    },
    userHasRole(requiredRole) {
      const userRole = localStorage.getItem('role');
      return userRole === requiredRole;
    }
  }
};
</script>


<style scoped>

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.event-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 600px; /* Максимальная ширина формы */
}

.form-group {
  width: 100%;
  margin-bottom: 20px; /* Отступ между полями ввода */
}

.input-style {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: 2px solid #ffffff;
  border-radius: 5px;
  background: transparent;
  color: white;
  font-size: 1em;
  outline: none;
  transition: all 0.3s ease;
}

.input-style:focus {
  border-color: #aaa; /* Цвет границы при фокусе */
}

.create-button {
  padding: 10px 20px;
  border: 2px solid #ffffff;
  border-radius: 5px;
  background: transparent;
  color: white;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

.create-button:hover {
  color: #000;
  background-color: #ffffff;
}


.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.header > div {
  display: flex;
  flex-direction: column; /* Расположение дочерних элементов в столбец */
}

.header > div > div {
  margin-bottom: 30px; /* Отступ между группами кнопок */
}

.brand {
  font-size: 2em; /* Увеличить размер шрифта */
  font-weight: bold; /* Сделать шрифт жирным */
  color: white; /* Изменить цвет на белый */
}

.login-button,
.register-button,
.admin-button {
  margin-right: 10px;
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

.login-button:hover,
.register-button:hover,
.admin-button:hover {
  color: #000;
  background-color: #ffffff;
}

</style>
