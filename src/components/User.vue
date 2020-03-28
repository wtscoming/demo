<template>
    <div class="user">
        <b-navbar type="dark" variant="dark">
            <b-navbar-nav>
                <b-nav-item @click="back">
                    <i class="fas fa-angle-double-left"></i>
                    <span>返回</span>
                </b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-nav-item @click="del" :disabled="!team_info.name">
                    <i class="fas fa-trash-alt"></i>
                    <span>删除</span>
                </b-nav-item>
                <b-nav-item @click="save" :disabled="!team_info.name">
                    <i class="fas fa-save"></i>
                    <span>保存</span>
                </b-nav-item>
            </b-navbar-nav>
        </b-navbar>
        <b-overlay :show="loading" rounded="sm">
            <div class="container">
                <br>
                <h2 class="text-center">{{ team_info.name }}</h2>
                <br>
                <div class="clearfix">
                    <b-img width="110" height="100" left :src="img_url(4, team_info.face4)" @click="edit(4)"></b-img>
                    <b-img width="110" height="100" right :src="img_url(2, team_info.face2)" @click="edit(2)"></b-img>
                </div>
                <br>
                <div class="clearfix">
                    <b-img width="110" height="100" center :src="img_url(1, team_info.face1)" @click="edit(1)"></b-img>
                </div>
                <br>
                <div class="clearfix">
                    <b-img width="110" height="100" left :src="img_url(5, team_info.face5)" @click="edit(5)"></b-img>
                    <b-img width="110" height="100" right :src="img_url(3, team_info.face3)" @click="edit(3)"></b-img>
                </div>
                <br>
                <b-container>
                    <b-form-row class="text-center">
                        <b-col>
                            <b-button pill size="sm" @click="team_info.score -= 1000" :disabled="team_info.score < 1000" variant="danger">-1000</b-button>
                        </b-col>
                        <b-col>
                            <b-button pill size="sm" @click="team_info.score -= 100" :disabled="team_info.score < 100" variant="danger">-100</b-button>
                        </b-col>
                        <b-col>{{ team_info.score }}</b-col>
                        <b-col>
                            <b-button pill size="sm" @click="team_info.score += 100" variant="primary">+100</b-button>
                        </b-col>
                        <b-col>
                            <b-button pill size="sm" @click="team_info.score += 1000" variant="primary">+1000</b-button>
                        </b-col>
                    </b-form-row>
                </b-container>
            </div>
        </b-overlay>
        <b-modal v-model="visited" scrollable>
            <template v-slot:modal-header>
                <b-form inline>
                    <b-form-group label="属性" label-cols="4" label-size="sm">
                        <b-form-select v-model="type" :options="type_options" size="sm"></b-form-select>
                    </b-form-group>
                    <span>&nbsp;&nbsp;</span>
                    <b-form-group label="职业" label-cols="4" label-size="sm">
                        <b-form-select v-model="job" :options="job_options" size="sm"></b-form-select>
                    </b-form-group>
                </b-form>
            </template>
            <template v-slot:modal-footer="{ hide }">
                <b-button size="sm" variant="danger" @click="hide()">关闭</b-button>
            </template>
            <b-img-lazy thumbnail width="77" height="70" offset="40" v-for="(item, index) in filter_face" :key="index" :src="img_url(1, item.id)" @click.native="set_face(item.id)"></b-img-lazy>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios'
import { host } from '../config/host'
import { login_check, img_url } from '../common/utils'

export default {
    name: 'User',
    data() {
        return {
            guild_id: '', // 公会id
            team_id: '', // 队伍id
            team_info: {
                id: 1,
                name: '',
                face1: null,
                face2: null,
                face3: null,
                face4: null,
                face5: null,
                score: 0,
                update_time: 0,
                guild: 1
            }, // 队伍信息
            loading: false, // 加载中
            visited: false, // 模态框
            img_url, // 图片链接
            face_list: [], // 头像列表
            position: 1, // 站位
            type: '', // 属性
            type_options: [
                { value: '', text: '全部' },
                { value: '1', text: '水' },
                { value: '2', text: '火' },
                { value: '3', text: '树' },
                { value: '4', text: '雷' },
                { value: '5', text: '光' },
                { value: '6', text: '暗' },
            ],
            job: '', // 职业
            job_options: [
                { value: '', text: '全部' },
                { value: '1', text: '战士' },
                { value: '2', text: '刺客' },
                { value: '3', text: '射手' },
                { value: '4', text: '法师' },
                { value: '5', text: '牧师' },
            ]
        }
    },
    computed: {
        // 过滤头像
        filter_face() {
            let face_list = this.face_list
            if (this.type) {
                face_list = face_list.filter(item => item.type === this.type)
            }
            if (this.job) {
                face_list = face_list.filter(item => item.job === this.job)
            }
            return face_list
        }
    },
    methods: {
        // 返回上一页
        back() {
            this.$router.go(-1)
        },
        // 查询队伍信息
        get_team_info() {
            const params = {
                id: this.team_id
            }
            axios.get(`${host}/user`, { params }).then(res => {
                if (res.data) {
                    this.team_info = res.data
                }
            })
        },
        // 获取头像列表
        get_face_list() {
            axios.get(`${host}/face`).then(res => {
                if (res.data) {
                    this.face_list = res.data
                }
            })
        },
        // 删除队伍
        del() {
            this.$bvModal.msgBoxConfirm('是否删除队伍信息?', {
                title: '请确认',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: '删除',
                cancelTitle: '取消',
                footerClass: 'p-2',
                hideHeaderClose: false,
                centered: true
            }).then(val => {
                if (val) {
                    const params = {
                        id: this.team_id
                    }
                    axios.get(`${host}/delete`, { params }).then(res => {
                        if (res.data) {
                            this.back() // 前进bug暂时不解决
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
        },
        // 保存队伍
        save() {
            const now = new Date()
            this.team_info.update_time = now.getTime()
            this.loading = true
            axios.post(`${host}/update`, this.team_info).then(res => {
                this.loading = false
                if (res.data) {
                    this.back()
                }
            }).catch(err => {
                this.loading = false
            })
        },
        // 编辑队伍
        edit(position = 1) {
            const face_id = this.team_info[`face${position}`]
            if (face_id) {
                const face_item = this.face_list.find(item => item.id === face_id)
                if (face_item) {
                    this.type = face_item.type
                    this.job = face_item.job
                }
            } else {
                this.type = ''
                this.job = ''
            }
            this.position = position
            this.visited = true
        },
        // 设置头像
        set_face(id = 999) {
            this.team_info[`face${this.position}`] = id
            this.visited = false
        }
    },
    created() {
        // 初始化
        this.guild_id = this.$route.query.id
        this.team_id = this.$route.query.team
        if (this.guild_id && login_check(this.guild_id)) {
            this.get_team_info()
            this.get_face_list()
        } else {
            this.$router.replace('/')
        }
    }
}
</script>
