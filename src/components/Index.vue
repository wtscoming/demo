<template>
    <div class="index container">
        <h2 class="text-center">公会列表</h2>
        <b-list-group>
            <b-list-group-item button v-for="(item, index) in list" :key="index" @click="login(String(item.id))">
                <b-navbar type="dark" variant="dark">
                    <b-navbar-brand>{{ item.name }}</b-navbar-brand>
                </b-navbar>
            </b-list-group-item>
            <b-list-group-item button class="text-center" @click="create">
                <i class="fas fa-plus"></i>
                <span>新建</span>
            </b-list-group-item>
        </b-list-group>
        <b-modal v-model="visited" :title="title" hide-footer>
            <b-overlay :show="loading" rounded="sm">
                <b-form-group description="请输入不超过10位的字符组合">
                    <b-form-input :type="type" :placeholder="placeholder" v-model.trim="value" :state="state" @focus="state = null" @blur="validate" spellcheck="false"></b-form-input>
                </b-form-group>
                <b-button block variant="success" @click="submit">确 认</b-button>
                <b-button block variant="danger" @click="visited = false">取 消</b-button>
            </b-overlay>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios'
import { host } from '../config/host'
import { login_check } from '../common/utils'

export default {
    name: 'Index',
    data() {
        return {
            list: [], // 公会列表
            visited: false, // 模态框
            loading: false, // 加载中
            id: '', // 公会id
            title: '', // 模态框标题
            type: 'text', // 输入框类型
            placeholder: '请输入...', // 占位符
            value: '', // 输入值
            state: null, // 输入框状态
        }
    },
    methods: {
        // 获取公会列表
        get_list() {
            axios.get(`${host}/guild`).then(res => {
                if (res.data) {
                    this.list = res.data
                }
            })
        },
        // 新建公会
        create() {
            this.id = ''
            this.title = '新建公会'
            this.type = 'text'
            this.placeholder = '请输入公会名'
            this.value = ''
            this.state = null
            this.visited = true
        },
        // 输入框校验
        validate() {
            if (this.value.length === 0 || this.value.length > 10) {
                this.state = false
            } else {
                this.state = true
            }
            return this.state
        },
        // 表单提交
        submit() {
            if (!this.validate()) {
                return
            }
            if (this.title === '新建公会') {
                const params = {
                    name: this.value
                }
                this.loading = true
                axios.post(`${host}/create`, params).then(res => {
                    this.loading = false
                    if (res.data) {
                        const id = String(res.data)
                        sessionStorage.login = id
                        this.login(id)
                    }
                }).catch(err => {
                    this.loading = false
                })
            } else {
                const params = {
                    id: this.id,
                    password: this.value
                }
                this.loading = true
                axios.post(`${host}/login`, params).then(res => {
                    this.loading = false
                    if (res.data > 0) {
                        sessionStorage.login = this.id
                        this.login(this.id)
                    } else {
                        this.$bvToast.toast('身份验证失败', {
                            title: '错误',
                            variant: 'danger',
                            solid: true,
                            toaster: 'b-toaster-top-center',
                            autoHideDelay: 1000
                        })
                    }
                }).catch(err => {
                    this.loading = false
                })
            }
        },
        // 登录公会
        login(id = '') {
            if (!login_check(id)) {
                this.id = id
                this.title = '登录验证'
                this.type = 'password'
                this.placeholder = '请输入公会密码'
                this.value = ''
                this.state = null
                this.visited = true
            } else {
                this.$router.push({
                    path: '/home',
                    query: { id }
                })
            }
        }
    },
    created() {
        // 初始化
        this.get_list()
    }
}
</script>
