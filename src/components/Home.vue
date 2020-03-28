<template>
    <div class="home">
        <div class="container">
            <b-link @click="back">
                <i class="fas fa-angle-double-left"></i>
                <span>返回</span>
            </b-link>
        </div>
        <h1 class="text-center">{{ name }}</h1><br>
        <b-list-group class="text-center">
            <b-list-group-item>
                <router-link :to="{ path: '/register', query: { id } }">战力填报</router-link>
            </b-list-group-item>
            <b-list-group-item>
                <router-link :to="{ path: '/defender', query: { id } }">布防详情</router-link>
            </b-list-group-item>
            <b-list-group-item>
                <router-link :to="{ path: '/deploy', query: { id } }">防御部署</router-link>
            </b-list-group-item>
            <b-list-group-item>
                <router-link :to="{ path: '/password', query: { id } }">修改密码</router-link>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
import axios from 'axios'
import { host } from '../config/host'
import { login_check } from '../common/utils'

export default {
    name: 'Home',
    data() {
        return {
            id: '', // 公会id
            name: '', // 公会名
        }
    },
    methods: {
        // 查询公会名
        get_name() {
            const params = {
                id: this.id
            }
            axios.get(`${host}/home`, { params }).then(res => {
                if (res.data) {
                    this.name = res.data
                }
            })
        },
        // 返回上一页
        back() {
            this.$router.go(-1)
        }
    },
    created() {
        // 初始化
        this.id = this.$route.query.id
        if (this.id && login_check(this.id)) {
            this.get_name()
        } else {
            this.$router.replace('/')
        }
    }
}
</script>
