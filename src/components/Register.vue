<template>
    <div class="register container">
        <div>
            <b-link @click="back">
                <i class="fas fa-angle-double-left"></i>
                <span>返回</span>
            </b-link>
        </div>
        <b-list-group>
            <b-list-group-item v-for="(item, index) in list" :key="index">
                <div class="clearfix">
                    <b>{{ item.name }}</b>
                    <b-link class="edit" @click="edit(item.id)">
                        <i class="fas fa-edit"></i>
                        <span>编辑</span>
                    </b-link>
                </div>
                <b-container>
                    <b-form-row>
                        <b-col v-for="num in 5" :key="`face${num}`">
                            <img width="44" height="40" :src="img_url(num, item[`face${num}`])">
                        </b-col>
                    </b-form-row>
                </b-container>
                <div class="clearfix">
                    <span>
                        <i class="fas fa-fire-alt"></i>
                        <b>{{ item.score }}</b>
                    </span>
                    <span :class="['update-time', { 'error': overtime(item.update_time) }]">{{ time_format(item.update_time) }}</span>
                </div>
            </b-list-group-item>
            <b-list-group-item button class="text-center" @click="add">
                <i class="fas fa-plus"></i>
                <span>添加</span>
            </b-list-group-item>
        </b-list-group>
        <b-modal v-model="visited" hide-footer title="创建队伍">
            <b-overlay :show="loading" rounded="sm">
                <b-form-group description="请输入不超过10位的字符组合">
                    <b-form-input placeholder="请输入队伍名" v-model.trim="name" :state="state" @focus="state = null" @blur="validate" spellcheck="false"></b-form-input>
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
import { login_check, img_url, time_format } from '../common/utils'

export default {
    name: 'Register',
    data() {
        return {
            id: '', // 公会id
            list: [], // 队伍列表
            visited: false, // 模态框
            loading: false, // 加载中
            name: '', // 队伍名
            state: null, // 队伍名校验
            img_url, // 图片链接
            time_format, // 时间格式化
        }
    },
    methods: {
        // 返回上一页
        back() {
            this.$router.go(-1)
        },
        // 获取队伍信息
        get_list() {
            const params = {
                id: this.id
            }
            axios.get(`${host}/team`, { params }).then(res => {
                if (res.data) {
                    this.list = res.data
                }
            })
        },
        // 添加队伍
        add() {
            this.name = ''
            this.state = null
            this.visited = true
        },
        // 数据校验
        validate() {
            if (this.name.length === 0 || this.name.length > 10) {
                this.state = false
            } else {
                this.state = true
            }
            return this.state
        },
        // 提交数据
        submit() {
            if (!this.validate()) {
                return
            }
            const now = new Date()
            const params = {
                name: this.name,
                update_time: now.getTime(),
                guild: this.id
            }
            this.loading = true
            axios.post(`${host}/insert`, params).then(res => {
                this.loading = false
                if (res.data) {
                    this.$router.push({
                        path: '/user',
                        query: {
                            id: this.id,
                            team: res.data
                        }
                    })
                }
            }).catch(err => {
                this.loading = false
            })
        },
        // 超时检查
        overtime(timestamp) {
            const now = new Date()
            const limit = 2 * 24 * 60 * 60 * 1000 // 默认2天
            if (now.getTime() - timestamp > limit) {
                return true
            }
            return false
        },
        // 编辑队伍
        edit(team_id = 1) {
            this.$router.push({
                path: '/user',
                query: {
                    id: this.id,
                    team: team_id
                }
            })
        }
    },
    created() {
        // 初始化
        this.id = this.$route.query.id
        if (this.id && login_check(this.id)) {
            this.get_list()
        } else {
            this.$router.replace('/')
        }
    }
}
</script>

<style scoped>
.edit {
    float: right;
}

img {
    border-radius: 50%;
}

.update-time {
    float: right;
    color: green;
}

.error {
    color: red;
}
</style>
