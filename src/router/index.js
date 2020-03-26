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
