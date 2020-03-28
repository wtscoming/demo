import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

export default new VueRouter({
    routes: [
        {
            path: '/',
            component: resolve => require(['../components/Index.vue'], resolve)
        },
        {
            path: '/home',
            component: resolve => require(['../components/Home.vue'], resolve)
        },
        {
            path: '/password',
            component: resolve => require(['../components/Password.vue'], resolve)
        },
        {
            path: '/register',
            component: resolve => require(['../components/Register.vue'], resolve)
        },
        {
            path: '/user',
            component: resolve => require(['../components/User.vue'], resolve)
        },
        {
            path: '/defender',
            component: resolve => require(['../components/Defender.vue'], resolve)
        },
        {
            path: '/deploy',
            component: resolve => require(['../components/Deploy.vue'], resolve)
        },
        {
            path: '/error',
            component: resolve => require(['../components/NotFound.vue'], resolve)
        },
        {
            path: '*',
            redirect: '/error'
        }
    ],
    scrollBehavior() {
        return {
            x: 0,
            y: 0
        }
    }
})
