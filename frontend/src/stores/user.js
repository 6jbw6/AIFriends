import {defineStore} from "pinia";
import { ref } from "vue";
export const useUserStore=defineStore('user',()=>{
    const id=ref(1)
    const username=ref('jbw')
    const photo=ref('http://127.0.0.1:8000/media/user/photos/default.png')
    const profile=ref('111')
    const accessToken=ref('111')
    function isLogin()
    {
        return !!accessToken.value      //必须带value!!!
    }
    function setAccessToken(token)
    {
        accessToken.value=token
    }
    function setUserInfo(data)
    {
        id.value=data.id
        username.value=data.username
        photo.value=photo
        profile.value=profile
    }
    function Logout()
    {
        id.value=0
        username.value=''
        photo.value=''
        profile.value=''
    }
    return{
        id,
        username,
        photo,
        profile,
        accessToken,
        isLogin,
        setAccessToken,
        setUserInfo,
        Logout
    }
})