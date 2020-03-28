<template>
    <div class="password">
        <b-navbar type="dark" variant="dark">
            <b-navbar-nav>
                <b-nav-item @click="back">
                    <i class="fas fa-angle-double-left"></i>
                    <span>返回</span>
                </b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-nav-item @click="save">
                    <i class="fas fa-save"></i>
                    <span>保存</span>
                </b-nav-item>
            </b-navbar-nav>
        </b-navbar>
        <b-overlay :show="loading" rounded="sm">
            <div class="container">
                <br>
                <h2 class="text-center">修改密码</h2>
                <b-form>
                    <b-form-group label="原密码：" description="请输入不超过10位的字符组合">
                        <b-form-input type="password" v-model.trim="pre_passwd" :state="pre_passwd_valid" @focus="pre_passwd_valid = null" @blur="pre_passwd_validate"></b-form-input>
                    </b-form-group>
                    <b-form-group label="新密码：" description="请输入不超过10位的字符组合">
                        <b-form-input type="password" v-model.trim="new_passwd" :state="new_passwd_valid" @focus="new_passwd_valid = null" @blur="new_passwd_validate"></b-form-input>
                    </b-form-group>
                    <b-form-group label="确认密码：" description="请输入不超过10位的字符组合">
                        <b-form-input type="password" v-model.trim="confirm" :state="confirm_valid" @focus="confirm_valid = null" @blur="confirm_validate"></b-form-input>
                    </b-form-group>
                </b-form>
            </div>
        </b-overlay>
    </div>
</template>

<script>
import axios from 'axios'
import { host } from '../config/host'
import { login_check } from '../common/utils'

export default {
    name: 'Password',
    data() {
        return {
            id: '', // 公会id
            loading: false, // 加载中
            pre_passwd: '', // 原密码
            new_passwd: '', // 新密码
            confirm: '', // 确认密码
            pre_passwd_valid: null, // 原密码校验状态
            new_passwd_valid: null, // 新密码校验状态
            confirm_valid: null // 确认密码校验状态
        }
    },
    methods: {
        // 返回上一页
        back() {
            this.$router.go(-1)
        },
        // 保存
        save() {
            if (!this.validate()) {
                return
            }
            const params = {
                id: this.id,
                pre_passwd: this.pre_passwd,
                new_passwd: this.new_passwd
            }
            this.loading = true
            axios.post(`${host}/password`, params).then(res => {
                this.loading = false
                if (res.data) {
                    this.$bvModal.msgBoxOk('身份已过期, 请重新登录', {
                        title: '提示',
                        size: 'sm',
                        buttonSize: 'sm',
                        okVariant: 'success',
                        okTitle: '确认',
                        headerClass: 'p-2',
                        footerClass: 'p-2',
                        centered: true
                    }).then(val => {
                        sessionStorage.login = ''
                        this.$router.replace('/')
                    }).catch(err => {
                        sessionStorage.login = ''
                        this.$router.replace('/')
                    })
                } else {
                    this.$bvToast.toast('原密码错误', {
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
        },
        // 数据校验
        pre_passwd_validate() {
            if (this.pre_passwd.length === 0 || this.pre_passwd.length > 10) {
                this.pre_passwd_valid = false
            } else {
                this.pre_passwd_valid = true
            }
            return this.pre_passwd_valid
        },
        new_passwd_validate() {
            if (this.new_passwd.length === 0 || this.new_passwd.length > 10) {
                this.new_passwd_valid = false
            } else {
                this.new_passwd_valid = true
            }
            return this.new_passwd_valid
        },
        confirm_validate() {
            if (this.confirm.length === 0 || this.confirm.length > 10 || this.confirm !== this.new_passwd) {
                this.confirm_valid = false
            } else {
                this.confirm_valid = true
            }
            return this.confirm_valid
        },
        validate() {
            let success = true
            if (!this.pre_passwd_validate()) {
                success = false
            }
            if (!this.new_passwd_validate()) {
                success = false
            }
            if (!this.confirm_validate()) {
                success = false
            }
            return success
        }
    },
    created() {
        // 初始化
        this.id = this.$route.query.id
        if (!this.id || !login_check(this.id)) {
            this.$router.replace('/')
        }
    }
}
</script>
