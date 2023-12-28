import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        accessToken: null,
        userRole: null,
    },
    mutations: {
        setAccessToken(state, token) {
            state.accessToken = token;
        },
        setUserRole(state, role) {
            state.userRole = role;
        },
    },
    actions: {
        // Здесь могут быть асинхронные операции, которые затем вызывают мутации
    },
    getters: {
        // Здесь могут быть геттеры для доступа к состоянию
    },
});