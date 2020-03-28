//import { host } from '../config/host'

// 登录检查(或者路由拦截)
export function login_check(id = '') {
    if (!sessionStorage.login || sessionStorage.login !== id) {
        return false
    }
    return true
}

// 图片地址
export function img_url(index = 1, face = null) {
    if (face) {
        return `http://static.web.sdo.com/xuezu/pic/Blood/Cards/Pic/${face}.png`
    }
    return `/bloodline/assets/${index}.png`
}

// 时间格式化
export function time_format(timestamp = null) {
    if (!timestamp) {
        return 'yyyy-mm-dd hh:mm:ss'
    }
    const time = new Date(timestamp)
    const year = String(time.getFullYear())
    let month = time.getMonth() + 1
    if (month < 10) {
        month = `0${month}`
    }
    let date = time.getDate()
    if (date < 10) {
        date = `0${date}`
    }
    let hours = time.getHours()
    if (hours < 10) {
        hours = `0${hours}`
    }
    let minutes = time.getMinutes()
    if (minutes < 10) {
        minutes = `0${minutes}`
    }
    let seconds = time.getSeconds()
    if (seconds < 10) {
        seconds = `0${seconds}`
    }
    return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`
}
