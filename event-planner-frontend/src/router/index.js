import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import EventList from '@/components/EventList.vue';
import EventDetails from '@/components/EventDetails.vue';
import CreateEvent from '@/components/CreateEvent.vue';
import EventAdmin from '@/components/EventAdmin.vue';
import axios from 'axios';


Vue.use(Router);


function isTokenValid() {
  const token = localStorage.getItem('access_token');
  const expiresAt = localStorage.getItem('token_expires_at');
  return token && expiresAt && Date.now() < Number(expiresAt) * 1000;
}

const router =  new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/eventlist',
      name: 'EventList',
      component: EventList,
    },
    {
      path: '/event/:id',
      name: 'EventDetails',
      component: EventDetails,
      props: true,
    },
    {
      path: '/createevent',
      name: 'CreateEvent',
      component: CreateEvent,
    },
    {
      path: '/eventadmin',
      name: 'EventAdmin',
      component: EventAdmin,
    },
    // Добавьте другие маршруты
  ],
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/eventlist'];
  const authRequired = !publicPages.includes(to.path);
  const token  = localStorage.getItem('access_token');


  if (authRequired && (!token || !isTokenValid())) {
    return next('/login');
  }

  if (token && isTokenValid()) {
    console.log('router', token)
    axios.defaults.headers['Authorization'] = `Bearer ${token}`;
    Vue.prototype.$http.defaults.headers['Authorization'] = `Bearer ${token}`;
  }

  next();
});


export default router