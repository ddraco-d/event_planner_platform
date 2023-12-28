<template>
  <div class="event-list-container">

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



    <h1>Список событий</h1>

    <!-- Раздел с предстоящими событиями -->
    <div class="events-grid">
      <div v-for="event in upcomingEvents" :key="event.id" class="event-card">
        <img :src="event.image" alt="Изображение события" class="event-image">
        <h3 class="event-title">
          <router-link :to="{ name: 'EventDetails', params: { id: event.id } }" class="event-link">{{ event.title }}</router-link>
        </h3>
        <p class="event-location">{{ event.description }}</p>
        <!-- Добавьте эту строку для отображения даты события -->
        <p class="event-date">{{ new Date(event.date).toLocaleDateString() }}</p>
      </div>
    </div>

    <h2>Прошедшие события</h2>

    <!-- Раздел с прошедшими событиями -->
    <div class="events-grid past-events">
      <div v-for="event in pastEvents" :key="event.id" class="event-card past-event">
        <img :src="event.image" alt="Изображение события" class="event-image">
        <h3 class="event-title">
          <router-link :to="{ name: 'EventDetails', params: { id: event.id } }" class="event-link">{{ event.title }}</router-link>
        </h3>
        <p class="event-location">{{ event.description }}</p>
        <!-- Добавьте эту строку для отображения даты события -->
        <p class="event-date">{{ new Date(event.date).toLocaleDateString() }}</p>
      </div>
    </div>

  </div>
</template>


<script>
export default {
  data() {
    return {
      events: [
        { id: 1, title: 'Событие 1', description: 'Место 1', date: '2023-05-01T19:00:00', image: require('@/assets/test.jpg') },
        // { id: 2, title: 'Событие 2', description: 'Место 2', date: '2023-05-01T19:00:00', image: require('@/assets/test.jpg') },
        // Добавьте дополнительные события по мере необходимости
      ],
    };
  },
  computed: {
    upcomingEvents() {
      const now = new Date();
      return this.events.filter(event => event.date > now);
    },
    pastEvents() {
      const now = new Date();
      return this.events.filter(event => event.date <= now);
    },
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
          date: new Date(event.date),
          image: require('@/assets/test.jpg')
        }));
      } catch (error) {
        console.error("There was an error fetching the events:", error);
      }
    },
    userHasRole(requiredRole) {
      const userRole = localStorage.getItem('role');
      return userRole === requiredRole;
    }
  },
  created() {
    this.fetchEvents();
  },
};
</script>

<style scoped>

.event-date {
  margin: 0 10px 10px;
  font-size: 0.9em; /* Немного уменьшить размер шрифта для даты */
  color: #555; /* Цвет текста для даты */
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

/* Стили кнопок из Login.vue для согласованности */
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

/* Стили для прошедших событий */
.past-events .past-event {
  background-color: #e1e1e1; /* Серый фон */
  color: #666; /* Более темный цвет текста */
}

/* Стиль для заголовка раздела прошедших событий */
h2 {
  text-align: center;
  margin-top: 40px; /* Отступ сверху для заголовка */
}

.event-list-container {
  padding: 20px;
  //background-color: #007BFF; /* Синий фон */
  color: white; /* Белый текст для контраста */
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* Два столбца */
  grid-gap: 20px; /* Отступы между карточками */
}

.event-card {
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  overflow: hidden; /* Обрезка изображения по границе карточки */
  color: #333; /* Цвет текста внутри карточки */
}

.event-image {
  width: 100%;
  height: auto;
  display: block;
}

.event-title {
  margin: 10px;
}

.event-link {
  text-decoration: none;
  color: #007BFF;
}

.event-link:hover {
  text-decoration: underline;
}

.event-location {
  margin: 0 10px 10px;
  font-style: italic;
}
</style>