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
                <router-link :to="{ path: '/register', query: { id } }">
                    <i class="fas fa-pencil-alt"></i>
                    <span>战力填报</span>
                </router-link>
            </b-list-group-item>
            <b-list-group-item>
                <router-link :to="{ path: '/defender', query: { id } }">
                    <i class="fas fa-star"></i>
                    <span>布防详情</span>
                </router-link>
            </b-list-group-item>
            <b-list-group-item>
                <router-link :to="{ path: '/deploy', query: { id } }">
                    <i class="fas fa-shield-alt"></i>
                    <span>防御部署</span>
                </router-link>
            </b-list-group-item>
            <b-list-group-item>
                <router-link :to="{ path: '/password', query: { id } }">
                    <i class="fas fa-unlock"></i>
                    <span>修改密码</span>
                </router-link>
            </b-list-group-item>
            <b-list-group-item>
                <b-link @click="rename">
                    <i class="fas fa-scroll"></i>
                    <span>更改会名</span>
                </b-link>
            </b-list-group-item>
            <b-list-group-item>
                <b-link @click="dismiss">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>解散公会</span>
                </b-link>
            </b-list-group-item>
        </b-list-group>
        <b-modal v-model="visited" title="公会重命名">
            <b-overlay :show="loading" rounded="sm">
                <b-form-group description="请输入不超过10位的字符组合">
                    <b-form-input placeholder="请输入新的公会名" v-model.trim="new_name" :state="state" @focus="state = null" @blur="validate" spellcheck="false"></b-form-input>
                </b-form-group>
            </b-overlay>
            <template v-slot:modal-footer="{ hide }">
                <b-button size="sm" variant="danger" @click="hide()">关闭</b-button>
                <b-button size="sm" variant="success" @click="submit" :disabled="loading">确认</b-button>
            </template>
        </b-modal>
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
            visited: false, // 模态框
            loading: false, // 加载中
            new_name: '', // 新公会名
            state: null, // 数据校验
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
        },
        // 输入框校验
        validate() {
            if (this.new_name.length === 0 || this.new_name.length > 10) {
                this.state = false
            } else {
                this.state = true
            }
            return this.state
        },
        // 公会重命名
        rename() {
            this.state = null
            this.new_name = ''
            this.visited = true
        },
        // 提交表单
        submit() {
            if (!this.validate()) {
                return
            }
            const params = {
                id: this.id,
                name: this.new_name
            }
            this.loading = true
            axios.post(`${host}/rename`, params).then(res => {
                this.loading = false
                if (res.data) {
                    this.visited = false
                    this.get_name()
                } else {
                    // dosomething()
                }
            }).catch(err => {
                this.loading = false
            })
        },
        // 解散公会
        dismiss() {
            this.$bvModal.msgBoxConfirm('是否解散公会?', {
                title: '警告',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: '确认',
                cancelTitle: '取消',
                footerClass: 'p-2',
                hideHeaderClose: false,
                centered: true
            }).then(val => {
                if (val) {
                    const params = {
                        id: this.id
                    }
                    axios.get(`${host}/dismiss`, { params }).then(res => {
                        if (res.data) {
                            sessionStorage.login = ''
                            this.$router.replace('/')
                        }
                    }).catch(err => {
                        this.$bvToast.toast('操作失败', {
                            title: '错误',
                            variant: 'danger',
                            solid: true,
                            toaster: 'b-toaster-top-center',
                            autoHideDelay: 1000
                        })
                    })
                } else {
                    this.$bvToast.toast('取消操作', {
                        title: '提示',
                        variant: 'warning',
                        solid: true,
                        toaster: 'b-toaster-top-center',
                        autoHideDelay: 1000
                    })
                }
            })
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
