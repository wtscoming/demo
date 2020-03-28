<template>
    <div class="defender">
        <div class="container">
            <b-link @click="back">
                <i class="fas fa-angle-double-left"></i>
                <span>返回</span>
            </b-link>
        </div>
        <br>
        <b-container class="text-center">
            <b-form-row>
                <b-col><b>据点</b></b-col>
                <b-col><b>外墙</b></b-col>
                <b-col><b>内墙</b></b-col>
            </b-form-row>
            <b-form-row v-for="(item, i) in list" :key="i">
                <b-col v-for="(key, j) in Object.keys(item)" :key="j">
                    <template v-if="item[key]">
                        <div><i class="fas fa-angle-double-down"></i></div>
                        <div class="clearfix">
                            <b-img center :src="img_url(1, item[key].face1)" width="55" height="50"></b-img>
                        </div>
                        <div class="name">
                            <span>{{ `${i + 1}.${item[key].name}` }}</span>
                        </div>
                    </template>
                    <template v-else>
                        <br><br>
                    </template>
                </b-col>
            </b-form-row>
        </b-container>
    </div>
</template>

<script>
import axios from 'axios'
import { host } from '../config/host'
import { login_check, img_url } from '../common/utils'

export default {
    name: 'Defender',
    data() {
        return {
            id: '', // 公会id
            list: [], // 布防信息
            img_url, // 图片链接
        }
    },
    methods: {
        // 返回上一页
        back() {
            this.$router.go(-1)
        },
        // 获取队伍列表
        get_team() {
            const params = {
                id: this.id
            }
            axios.get(`${host}/team`, { params }).then(res => {
                if (res.data) {
                    this.set_team(res.data)
                }
            })
        },
        // 设置队伍信息
        set_team(team = []) {
            const params = {
                guild: this.id
            }
            axios.get(`${host}/defender`, { params }).then(res => {
                if (res.data) {
                    this.list = res.data.map(item => {
                        const data = {
                            hold1: null,
                            wall1: null,
                            wall2: null
                        }
                        if (item.hold1) {
                            data.hold1 = team.find(x => x.id === item.hold1) || null
                        }
                        if (item.wall1) {
                            data.wall1 = team.find(x => x.id === item.wall1) || null
                        }
                        if (item.wall2) {
                            data.wall2 = team.find(x => x.id === item.wall2) || null
                        }
                        return data
                    })
                }
            })
        }
    },
    created() {
        // 初始化
        this.id = this.$route.query.id
        if (this.id && login_check(this.id)) {
            this.get_team()
        } else {
            this.$router.replace('/')
        }
    }
}
</script>

<style scoped>
.defender {
    background-image: linear-gradient(#e66465, #9198e5);
}

img {
    border-radius: 50%;
}

.name > span {
    display: inline-block;
    width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
