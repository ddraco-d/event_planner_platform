<!-- EventAdmin.vue -->
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

    <h1>Администрирование событий</h1>
    <!-- Список событий с кнопками для удаления -->
    <div v-for="event in events" :key="event.id" class="event-item">
      <router-link :to="`/event/${event.id}`" class="login-button">{{ event.title }}</router-link>
      <button @click="deleteEvent(event.id)" class="admin-button">Удалить</button>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      events: [] // Массив событий
    };
  },
  created() {
    this.fetchEvents();
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await this.$http.get('/events/');
        // console.log('Response data:', response.data); // Добавьте это для отладки
        this.events = response.data.map(event => ({
          id: event.id,
          title: event.title,
          description: event.description,
          image: require('@/assets/test.jpg')
        }));
      } catch (error) {
        console.error("There was an error fetching the events:", error);
      }
    },
    async deleteEvent(eventId) {
      if (!this.userHasRole('admin')) {
        alert('Только администраторы могут удалять события.');
        return;
      }
      try {
        await this.$http.delete(`/events/${eventId}`);
        alert('Событие удалено!');
        // Обновление списка событий
      } catch (error) {
        console.error("Ошибка при удалении события:", error);
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

.event-item {
  /* Стили для элемента списка событий, если требуется */
  margin-left: 10px;
  margin-bottom: 10px; /* Пример отступа между пунктами списка */
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