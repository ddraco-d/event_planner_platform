<template>

  <div class="event-container" v-if="event">

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

    <div class="content-container">


      <h1>{{ event.title }}</h1>
      <img :src="event.image" alt="Изображение события" class="event-image">
      <p class="event-description">{{ event.description }}</p>
      <p class="event-date">Дата мероприятия: {{ formatDate(event.date) }}</p> <!-- Строка с датой -->
      <button
          @click="registerForEvent"
          :class="{'login-button': true, 'registered-button': isRegistered}"
      >
        {{ isRegistered ? 'Вы уже зарегистрировались' : 'Зарегистрироваться на событие' }}
      </button>
      <!-- Раздел комментариев -->
      <div class="comments-section">
        <h2>Комментарии</h2>
        <form @submit.prevent="submitComment">
          <textarea v-model="newComment" placeholder="Напишите комментарий..." required></textarea>
          <button type="submit" class="login-button">Отправить</button>
        </form>
        <div class="comments-list">
          <div class="comment" v-for="comment in comments" :key="comment.id">
            {{ comment.comment }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      event: {
        title: '',
        image: require('@/assets/test.jpg'),
        description: ''
      },
      newComment: '',
      comments: [],
      isRegistered: false, // Добавьте эту строку
    };
  },
  created() {
    // this.fetchEvent();
    // this.fetchComments();
    // this.checkRegistrationStatus();
    this.init();

  },
  methods: {
    async init() {
      await this.fetchEvent();
      this.fetchComments();
      this.checkRegistrationStatus();
    },

    async fetchEvent() {
      try {
        const response = await this.$http.get(`/events/${this.id}`);
        this.event = response.data;
        this.event.image = require('@/assets/test.jpg');
      } catch (error) {
        console.error("There was an error fetching the event data:", error);
      }
    },
    async registerForEvent() {
      try {
        // const token = this.$store.state.accessToken;
        await this.$http.post(`/tickets/${this.event.id}`, {});
        alert('Вы успешно зарегистрировались на событие!');
      } catch (error) {
        alert(error);
        console.error("Ошибка регистрации на событие:", error);
      }
    },
    async fetchComments() {
      try {
        const response = await this.$http.get(`/comments/${this.event.id}`);
        this.comments = response.data;
        // console.log(this.comments)
      } catch (error) {
        console.error("Ошибка при получении комментариев:", error);
      }
    },

    async submitComment() {
      if (!this.newComment.trim()) return; // Проверка на пустой комментарий

      try {
        const response = await this.$http.post(`/events/${this.event.id}/comments/`, {
          comment: this.newComment,
        });
        this.comments.push(response.data); // Добавить новый комментарий в список
        this.newComment = ''; // Очистить поле комментария после отправки
      } catch (error) {
        console.error("Ошибка при отправке комментария:", error);
      }
    },
    async checkRegistrationStatus() {
      try {
        const response = await this.$http.get(`/tickets/${this.event.id}`);
        this.isRegistered = response.data.has_ticket;
      } catch (error) {
        console.error("Ошибка при проверке статуса регистрации:", error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      // Используйте функцию форматирования из библиотеки или напишите свою
      // Например: return format(date, 'dd MMMM yyyy, HH:mm');
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },
    userHasRole(requiredRole) {
      const userRole = localStorage.getItem('role');
      return userRole === requiredRole;
    }
  },
};
</script>


<style scoped>



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
  margin-bottom: 20px; /* Отступ между группами кнопок */
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


.registered-button {
  background-color: #4CAF50; /* Пример цвета, вы можете выбрать свой */
  /* Другие стили для кнопки после регистрации */
}

.content-container {
  padding: 20px;
  max-width: 600px;
  margin: auto;
}

.event-image {
  width: 100%;
  height: auto;
  display: block;
}

.event-description {
  margin-top: 20px;
}
.register-button {
  margin-top: 20px;
  padding: 10px 20px;
  cursor: pointer;
}

.comments-section {
  margin-top: 40px;
}

.comments-list {
  margin-top: 20px;
}

.comment {
  color: black;
  background-color: #f0f0f0;
  padding: 10px;
  margin-bottom: 10px;
}

.submit-comment {
  margin-top: 10px;
  padding: 10px 20px;
  cursor: pointer;
}

/* Добавьте дополнительные стили по вашему усмотрению */
</style>