<template>
    <div class="deploy">
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
            <b-card no-body>
                <b-tabs card>
                    <b-tab title="据点" active>
                        <b-list-group>
                            <b-list-group-item v-for="(item, index) in set.hold1" :key="index">
                                <div class="clearfix">
                                    <b>{{ item.name }}</b>
                                    <span class="score">
                                        <i class="fas fa-fire-alt"></i>
                                        <b>{{ item.score }}</b>
                                    </span>
                                </div>
                                <b-container>
                                    <b-form-row>
                                        <b-col v-for="num in 5" :key="`face${num}`">
                                            <img width="44" height="40" :src="img_url(num, item[`face${num}`])">
                                        </b-col>
                                    </b-form-row>
                                </b-container>
                            </b-list-group-item>
                            <b-list-group-item button class="text-center" @click="add('hold1')" :disabled="set.hold1.length > 4">
                                <i class="fas fa-plus"></i>
                                <span>添加</span>
                            </b-list-group-item>
                        </b-list-group>
                    </b-tab>
                    <b-tab title="外墙">
                        <b-list-group>
                            <b-list-group-item v-for="(item, index) in set.wall1" :key="index">
                                <div class="clearfix">
                                    <b>{{ item.name }}</b>
                                    <span class="score">
                                        <i class="fas fa-fire-alt"></i>
                                        <b>{{ item.score }}</b>
                                    </span>
                                </div>
                                <b-container>
                                    <b-form-row>
                                        <b-col v-for="num in 5" :key="`face${num}`">
                                            <img width="44" height="40" :src="img_url(num, item[`face${num}`])">
                                        </b-col>
                                    </b-form-row>
                                </b-container>
                            </b-list-group-item>
                            <b-list-group-item button class="text-center" @click="add('wall1')" :disabled="set.wall1.length > 14">
                                <i class="fas fa-plus"></i>
                                <span>添加</span>
                            </b-list-group-item>
                        </b-list-group>
                    </b-tab>
                    <b-tab title="内墙">
                        <b-list-group>
                            <b-list-group-item v-for="(item, index) in set.wall2" :key="index">
                                <div class="clearfix">
                                    <b>{{ item.name }}</b>
                                    <span class="score">
                                        <i class="fas fa-fire-alt"></i>
                                        <b>{{ item.score }}</b>
                                    </span>
                                </div>
                                <b-container>
                                    <b-form-row>
                                        <b-col v-for="num in 5" :key="`face${num}`">
                                            <img width="44" height="40" :src="img_url(num, item[`face${num}`])">
                                        </b-col>
                                    </b-form-row>
                                </b-container>
                            </b-list-group-item>
                            <b-list-group-item button class="text-center" @click="add('wall2')" :disabled="set.wall2.length > 14">
                                <i class="fas fa-plus"></i>
                                <span>添加</span>
                            </b-list-group-item>
                        </b-list-group>
                    </b-tab>
                </b-tabs>
            </b-card>
        </b-overlay>
        <b-modal v-model="visited" hide-footer scrollable title="队伍列表">
            <b-list-group>
                <b-list-group-item button v-for="(item, index) in list" :key="index" @click="select(index)">
                    <div class="clearfix">
                        <b>{{ item.name }}</b>
                        <span class="score">
                            <i class="fas fa-fire-alt"></i>
                            <b>{{ item.score }}</b>
                        </span>
                    </div>
                    <b-container>
                        <b-form-row>
                            <b-col v-for="num in 5" :key="`face${num}`">
                                <img width="44" height="40" :src="img_url(num, item[`face${num}`])">
                            </b-col>
                        </b-form-row>
                    </b-container>
                </b-list-group-item>
            </b-list-group>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios'
import { host } from '../config/host'
import { login_check, img_url } from '../common/utils'

export default {
    name: 'Deploy',
    data() {
        return {
            id: '', // 公会id
            visited: false, // 模态框
            loading: false, // 加载中
            list: [], // 队伍列表
            set: {
                hold1: [], // 据点
                wall1: [], // 外墙
                wall2: [], // 内墙
            }, // 防御部署
            pos: 'hold1', // 建筑位置
            img_url, // 图片链接
        }
    },
    methods: {
        // 返回上一页
        back() {
            this.$router.go(-1)
        },
        // 保存设置
        save() {
            const params = {
                guild: this.id,
                ...this.set
            }
            this.loading = true
            axios.post(`${host}/deploy`, params).then(res => {
                this.loading = false
                if (res.data) {
                    this.back()
                }
            }).catch(err => {
                this.loading = false
            })
        },
        // 获取队伍列表
        get_list() {
            const params = {
                id: this.id
            }
            axios.get(`${host}/team`, { params }).then(res => {
                if (res.data) {
                    this.list = res.data.sort((a, b) => b.score - a.score)
                }
            })
        },
        // 添加队伍
        add(pos = 'hold1') {
            this.pos = pos
            this.visited = true
        },
        // 选择队伍
        select(index = 1) {
            const item = this.list[index]
            this.set[this.pos].push(item)
            this.visited = false
            this.list.splice(index, 1)
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
.score {
    float: right;
}

.score > b {
    display: inline-block;
    width: 50px;
}

img {
    border-radius: 50%;
}
</style>
